from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime, UTC
from typing import Annotated
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, defer
from authlib.integrations.starlette_client import OAuth
from jose import jwt, JWTError
from starlette.config import Config
from ..pymodels.schemas import GoogleUserBase
from ..pymodels.models import Usuario
from ..db.database import db_dependency
import os

ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Inicializar el esquema de seguridad HTTPBearer
http_bearer = HTTPBearer()

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None

if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise Exception('Missing env variables')

config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}

starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


def authenticate_user(email: str, password: str, db: type[Session]):
    user: Usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": email, "id": user_id}

    expires = datetime.now(UTC) + expires_delta

    encode.update({"exp": expires})

    return jwt.encode(encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)


def create_refresh_token(email: str, user_id: int, expires_delta: timedelta):
    return create_access_token(email, user_id, expires_delta)


def decode_token(token):
    return jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=ALGORITHM)
        email: str = payload.get("sub")
        user_id: int = payload.get("id")

        user: Usuario = db.query(Usuario).filter(Usuario.email == str(email)).options(defer(Usuario.google_sub)).first()

        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")

# Función para obtener el usuario actual a partir del token JWT
def get_current_user_http(db: db_dependency, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials
    try:
        # Decodificar el JWT
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")

        # Verificar que los datos estén presentes
        if not email or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o datos faltantes en el token."
            )
        # Buscar el usuario en la base de datos usando el email
        user: Usuario = db.query(Usuario).filter(Usuario.email == str(email)).options(
            defer(Usuario.google_sub),defer(Usuario.password_hash)).first()

        # Si el usuario no se encuentra en la base de datos, lanzamos un error
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado en la base de datos."
            )
        # Verificar si el user_id en el token coincide con el del usuario encontrado
        if user.id_usuario != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El ID del usuario en el token no coincide con el de la base de datos."
            )
        return user  # Devolvemos el objeto de usuario encontrado
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No es un token válido o ha expirado.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

def token_expired(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = decode_token(token)
        if not datetime.fromtimestamp(payload.get('exp'), UTC) > datetime.now(UTC):
            return True
        return False

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se puede validar al usuario.")


def get_user_by_google_sub(google_sub: int, db: Session):
    return db.query(Usuario).filter(Usuario.google_sub == str(google_sub)).first()


def create_user_from_google_info(google_user: GoogleUserBase, db: Session):
    apellidos = google_user.family_name
    nombre = google_user.given_name
    google_sub = google_user.sub
    email = google_user.email

    existing_user = db.query(Usuario).filter(Usuario.email == email).first()

    if existing_user:

        existing_user.google_id = google_sub
        db.commit()
        return existing_user
    else:

        new_user = Usuario(
            apellidos_familiar = apellidos,
            nombres = nombre,
            email=email,
            google_sub=google_sub,
            activo=False,
            esta_registrado=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


user_dependency = Annotated[dict, Depends(get_current_user)]
user_dependency_token = Annotated[dict, Depends(get_current_user_http)]