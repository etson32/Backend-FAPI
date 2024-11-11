from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from ..pymodels.models import Usuario
from ..pymodels.schemas import CreateUserRequestBase, GoogleUserBase, TokenBase, RefreshTokenRequestBase, UpdateUserRequestBase
from ._services import create_access_token, authenticate_user, bcrypt_context, create_refresh_token, \
    create_user_from_google_info, get_user_by_google_sub, token_expired, decode_token, user_dependency, get_current_user, get_current_user_http, user_dependency_token
from ..db.database import db_dependency
from ._services import oauth
from fastapi import Request
from fastapi.responses import RedirectResponse, JSONResponse
import os

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/callback/google"
FRONTEND_URL = os.getenv("FRONTEND_URL")


@router.get("/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)


@router.get("/callback/google")
async def auth_google(request: Request, db: db_dependency):
    try:
        user_response: OAuth2Token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user_info = user_response.get("userinfo")

    #print(user_info)

    google_user = GoogleUserBase(**user_info)

    existing_user = get_user_by_google_sub(google_user.sub, db)

    if existing_user:
        print("Existe el usuario")
        user = existing_user
    else:
        #Crear usuario temporal
        print("Creando usuario") 
        user = create_user_from_google_info(google_user, db)

    access_token = create_access_token(user.email, user.id_usuario, timedelta(days=7))
    refresh_token = create_refresh_token(user.email, user.id_usuario, timedelta(days=14))

    response = JSONResponse(content={#"message": "tokens en cookies",
                                     "access_token": access_token,
                                     "refresh_token": refresh_token}
                            )
    #response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    #response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)
    return response
    #return RedirectResponse(f"{FRONTEND_URL}auth?access_token={access_token}&refresh_token={refresh_token}")


# Endpoint para verificar usuario
@router.put("/verify-sign-up", status_code=status.HTTP_303_SEE_OTHER)
async def complete_registration(
    current_user: Usuario = Depends(get_current_user_http)  # Dependencia de la función get_current_user_http
):
    # Verificar si el usuario necesita completar su registro
    if not current_user.esta_registrado:
        return RedirectResponse(f"{FRONTEND_URL}complete-registration", status_code=status.HTTP_303_SEE_OTHER)
    # Verificar si el usuario está inactivo
    if not current_user.activo:
            raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="El usuario está inactivo y no tiene permiso para acceder."
    )
    # Redireccionar al frontend si todo está correcto
    return RedirectResponse(FRONTEND_URL, status_code=status.HTTP_303_SEE_OTHER)

# Endpoint para actualizar la información del usuario
@router.put("/complete-registration", status_code=status.HTTP_200_OK)
async def complete_registration(
    db: db_dependency,
    update_user_request: UpdateUserRequestBase,
    current_user: Usuario = Depends(get_current_user_http)  # Dependencia de la función get_current_user_http
):
    # Asegurarse que el usuario autenticado es el que está intentando actualizar su registro
    if current_user.esta_registrado and current_user.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario registrado y activo")

    # Asignar los valores obligatorios directamente
    current_user.password_hash = bcrypt_context.hash(update_user_request.password)
    current_user.dni = update_user_request.dni
    current_user.grado_academico = update_user_request.grado_academico
    current_user.id_rol = update_user_request.id_rol

    # Marcar al usuario como activo
    current_user.activo = True

    # Marcar al usuario como registrado
    current_user.esta_registrado = True

    # Guardar los cambios en la base de datos
    db.commit()

    return {"message": "Datos de Usuario registrado correctamente"}


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequestBase):
    create_user_model = Usuario(
        #username=create_user_request.username,
        password_hash=bcrypt_context.hash(create_user_request.password)
    )

    db.add(create_user_model)
    db.commit()

    return create_user_request


@router.get("/get-user", status_code=status.HTTP_201_CREATED)
async def get_user(db: db_dependency, user: user_dependency_token):
    return user


@router.post("/token", response_model=TokenBase, status_code=status.HTTP_200_OK)
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No es un usuario valido.")

    access_token = create_access_token(user.email, user.id_usuario, timedelta(days=7))
    refresh_token = create_refresh_token(user.email, user.id_usuario, timedelta(days=14))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenBase)
async def refresh_access_token(db: db_dependency, refresh_token_request: RefreshTokenRequestBase):
    token = refresh_token_request.refresh_token

    if token_expired(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expiró.")

    user = decode_token(token)

    access_token = create_access_token(user["sub"], user["id"], timedelta(days=7))
    refresh_token = create_refresh_token(user["sub"], user["id"], timedelta(days=14))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}