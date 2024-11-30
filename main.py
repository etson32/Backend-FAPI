from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.data_initializer import initialize_default_data
from app.db.database import engine, get_db, db_dependency
from app.pymodels import models
from app.pymodels import schemas
from app.routers.auth import router as auth_router
from app.routers.tesis import router as tesis_router
from app.routers.notification import router as notification_router
from app.routers._services import user_dependency
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security.api_key import APIKeyHeader
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List
from dotenv import load_dotenv
import shutil, logging, os

# Cargar las variables del archivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

origins = ["*"]

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator :
    print("Iniciando la aplicación...")
    # Crear las tablas si no existen
    models.Base.metadata.create_all(bind=engine)
    # Inicializar datos por defecto
    await initialize_default_data()
    yield
    # Código que se ejecuta al cerrar
    print("Cerrando la aplicación...")
    
# Crear la aplicación FastAPI con el contexto de vida
app = FastAPI(lifespan=lifespan)

# Define API Key Header para "Authorization"
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth_router)
app.include_router(tesis_router)
app.include_router(notification_router)

########################################################
 
########################################################

# @app.get("/", status_code=status.HTTP_200_OK)
# async def user(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication failed.")

#     return {"user": user}


@app.post("/roles/", tags=["Roles"])
async def crear_rol(rol: schemas.RolBase, db: Session = Depends(get_db)):
    # Verificar si el rol ya existe
    existing_rol = db.query(models.Rol).filter(models.Rol.nombre_rol == rol.nombre_rol).first()
    if existing_rol:
        raise HTTPException(status_code=400, detail="El rol ya existe.")

    db_rol = models.Rol(
        nombre_rol=rol.nombre_rol,
        descripcion=rol.descripcion,
    )

    # Validar que se está agregando
    try:
        db.add(db_rol)
        db.commit()  # Confirmar cambios en la base de datos
        db.refresh(db_rol)  # Obtener los datos actualizados del rol
        return {
            'detail': 'Rol creado con éxito',
            'rol_id': db_rol.id_rol  # Retornar el ID del nuevo rol
        }
    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(status_code=500, detail=str(e))  # Retornar un error 500

########################################################
########       USUARIOS
########################################################
# Endpoint par agregar usuario (BASICO)
@app.post("/usuario/", tags=["Usuarios"])
async def crear_usuario(usuario: schemas.UsuarioBase, db: Session = Depends(get_db)):
    db_usuario = models.Usuario(
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        nombres=usuario.nombres,
        correo_electronico=usuario.correo_electronico,
        dni=usuario.dni,
        password_hash=usuario.password_hash,
        grado_academico = usuario.grado_academico,
        activo=usuario.activo,
        id_rol=usuario.id_rol,  # Relación con la tabla Roles
    )

    # Validar que se está agregando
    try:
        db.add(db_usuario)
        db.commit()  # Confirmar cambios en la base de datos
        db.refresh(db_usuario)  # Obtener los datos actualizados del usuario
        return {
            'detail': 'Usuario creado con éxito',
            'usuario_id': db_usuario.id_usuario  # Retornar el ID del nuevo usuario si es necesario
        }
    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(status_code=500, detail=str(e))  # Retornar un error 500

# Endpoint para obtener usuario
@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioBase, tags=["Usuarios"])
async def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    # Buscar el usuario por ID en la base de datos
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Retornar solo los campos deseados en un diccionario
    return JSONResponse(content={
        "id": usuario.id_usuario,
        "dni": usuario.dni,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "nombres": usuario.nombres,
        "correo_electronico": usuario.correo_electronico,
        "activo": usuario.activo,
        "id_rol": usuario.id_rol
    })

# Endpoint para obtener todos los usuarios
@app.get("/usuarios/", response_model=List[schemas.UsuarioBase], tags=["Usuarios"])
async def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()  # Seleccionar todos los usuarios
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    
    return usuarios  # Retorna la lista de usuarios




# Endpoint para obtener todos los usuarios
@app.get("/docentes", response_model=List[schemas.UsuarioBase], tags=["Usuarios"])
async def obtener_docentes(db: Session = Depends(get_db)):
    docente_rol_id = db.query(models.Rol.id_rol).filter(models.Rol.nombre_rol == 'Docente').scalar()
    # Realizar la consulta solo para los campos necesarios
    docentes = db.query(
        models.Usuario.id_usuario,
        models.Usuario.apellido_paterno,
        models.Usuario.apellido_materno,
        models.Usuario.nombres,
        models.Usuario.grado_academico,
        models.Usuario.activo
    ).filter(models.Usuario.id_rol == docente_rol_id).all()

    if not docentes:
        raise HTTPException(status_code=404, detail="No se encontraron docentes")

    # Convertir el resultado en una lista de diccionarios
    # Crear la respuesta en formato JSON
    response = [
        {
            "id_usuario": id_usuario,
            "apellido_paterno": apellido,
            "apellido_materno": apellido_materno,
            "nombres": nombres,
            "grado_academico": grado_academico,
            "activo": activo,
        }
        for (id_usuario, apellido, apellido_materno, nombres, grado_academico, activo) in docentes
    ]
    return JSONResponse(content=response)  # Usar JSONResponse para devolver la respuesta

 
@app.put("/usuarios/{usuario_id}", tags=["Usuarios"])
async def editar_usuario(usuario_id: int, usuario: schemas.UsuarioBase, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar solo los campos que se proporcionan
    campos_a_actualizar = {
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "nombres": usuario.nombres,
        #"correo_electronico": usuario.correo_electronico,
        "dni": usuario.dni
        #"password_hash": usuario.password_hash,
        #"activo": usuario.activo,
        #"id_rol": usuario.id_rol
    }

    # Actualizar campos solo si no son None
    for campo, valor in campos_a_actualizar.items():
        if valor is not None:
            setattr(db_usuario, campo, valor)

    try:
        db.commit()  # Confirmar cambios en la base de datos
        db.refresh(db_usuario)  # Obtener los datos actualizados del usuario
        return {
            'detail': 'Usuario actualizado con éxito',
            'usuario_id': db_usuario.id_usuario
        }
    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(status_code=500, detail=str(e))  # Retornar un error 500
    

########################################################
########       USUARIOS
########################################################

# @app.post("/propuestatesis/", tags=["PlanTesis"])
# async def crear_propuestatesis(propuesta: schemas.TesisBase, db: Session = Depends(get_db)):
#     db_propuesta = models.PropuestaTesis(
#         titulo_tentativo=propuesta.titulo_tentativo,
#         descripcion=propuesta.descripcion,
#         keywords=propuesta.keywords,
#         asesor=propuesta.asesor, 
#         estado=propuesta.estado,
#         path_tesis=propuesta.path_tesis, # Path de la tesis
#         # fecha_inscripcion=propuesta.fecha_inscripcion,  # Fecha de inscripción, por defecto la actual
#         # fecha_modificacion=propuesta.fecha_modificacion  # Fecha de modificación, por defecto la actual
#     )
#     # Validar que se esta agregando
#     try:
#         db.add(db_propuesta)
#         db.commit()
#         db.refresh(db_propuesta)
#         return {
#             'detail': 'Success',
#         }
#     except Exception as e:
#         db.rollback()  # Revertir la transacción en caso de error
#         raise HTTPException(status_code=500, detail=str(e))  # Retornar un error 500


# #SUBIR ARCHIVO .txt
# # @app.post('/files', tags=["PlanTesis"])
# # def get_file(file: bytes = File(...)):
# #     content = file.decode('utf-8')
# #     lines = content.split('\n')
# #     return {"content": lines}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

# #Subir archivos, restringir a .PDF
# @app.post('/upload_propuesta', tags=["PlanTesis"])
# async def upload_file(uploaded_file: UploadFile = File(...)):
#     # Verifica la extensión del archivo
#     if not allowed_file(uploaded_file.filename):
#         raise HTTPException(status_code=400, detail="Extensión de archivo no válida. Solo se admite .pdf")
    
#     # Renombrar el archivo
#     new_name = "01-PT-2024-2.pdf"
#     path_d = "files/"+new_name
    
#     # Guarda el archivo directamente en el destino
#     with open(path_d, "wb") as buffer:
#         shutil.copyfileobj(uploaded_file.file, buffer)

#     ## GUARDAR PATH DE PLAN DE TESIS

#     return {
#         'filename': uploaded_file.filename,
#         'content_type': uploaded_file.content_type,
#         'path': path_d,
#         'detail': 'Success'
#     }

# @app.get("/propuestatesis/{propuesta_id}", tags=["PlanTesis"])
# async def get_propuesta_by_id(id_tesis: int, db: Session = Depends(get_db)):
#     propuesta = db.query(models.Tesis).filter(models.Tesis.id_tesis == id_tesis).first()
#     if propuesta is None:
#         raise HTTPException(status_code=404, detail="Propuesta de tesis no encontrada")
#     return propuesta

# Lanzar configuracion automatica para ejecucion
# Para pruebas locales

if __name__ == '__main__':
   import uvicorn
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
