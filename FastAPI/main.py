from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import List, Annotated, Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session, sessionmaker
import shutil, os, datetime
from datetime import datetime, timezone, timedelta
import uvicorn
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from data_initializer import initialize_default_data
from sqlalchemy import select, union_all, func

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

# Agregar datos por defecto
class TesisBase(BaseModel):
    titulo: str  # Título de la tesis
    resumen: str  # Resumen o abstract de la tesis
    especialidad: str  # Especialidad de la carrera
    keywords: Optional[str] = None  # Temas relacionados
    autor1: int  # ID del primer autor
    autor2: Optional[int] = None  # ID del segundo autor (opcional)
    autor3: Optional[int] = None  # ID del tercer autor (opcional)
    asesor: int  # ID del asesor
    actividad_focus: str  # Actividad actual de la tesis
    revisor1: Optional[int] = None  # ID del primer revisor (opcional)
    revisor2: Optional[int] = None  # ID del segundo revisor (opcional)
    asesorado: bool = False  # Estado de asesoramiento
    creacion_en: Optional[datetime] = None  # Fecha de creación de tesis
    editado_en: Optional[datetime] = None  # Fecha de última edición

class PlanTesisBase(BaseModel):
    id_tesis: int
    estado: str  # 'Visto', 'Observado', 'Aprobado', 'Rechazado'
    direccion_pdf: str
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None

class RevisarTesisBase(BaseModel):
    id_plan_tesis: int
    descripcion: str
    completado: bool = False
    fecha_creacion: datetime
    fecha_completado: Optional[datetime] = None
    origen_entidad: str  # 'Propuesta', 'Plan'

class DocumentosBase(BaseModel):
    id_tesis: int
    nombre_archivo: str
    detalle: Optional[str] = None
    tipo: str  # 'Oficio', 'Resolucion', 'Proveido', 'Informe Turnitin'
    create_by: int
    create_at: datetime
    update_at: Optional[datetime] = None
    fase: Optional[str] = None
    estado: str  # 'Activo', 'Inactivo', 'Rechazado'
    direccion_url: str

class RolBase(BaseModel):
    nombre_rol: str  # Nombre del rol (Ej.: Estudiante, Asesor, Secretario)
    descripcion: Optional[str] = None  # Descripción de las responsabilidades de ese rol

class UsuarioBase(BaseModel):
    apellido_paterno: str  # Apellido paterno del usuario
    apellido_materno: str  # Apellido materno del usuario
    nombres: str  # Nombres del usuario
    correo_electronico: str  # Correo electrónico usado para el login
    dni: str  # Documento de identidad
    password_hash: str  # Contraseña cifrada para autenticación
    grado_academico : str # Grado academico de usuario
    activo: bool = True  # Indica si el usuario está activo o inactivo
    id_rol: int  # Relación con la tabla Roles

class PermisoBase(BaseModel):
    nombre_permiso: str  # Nombre del permiso (Ej.: Crear Propuesta, Revisar Plan)
    descripcion: Optional[str] = None  # Descripción del permiso

class RolPermisoBase(BaseModel):
    id_rol: int  # Referencia al identificador del rol
    id_permiso: int  # Referencia al identificador del permiso
    # fecha_asignacion: datetime  # Fecha en que se asignó el permiso al rol


# Agregar datos por defecto
# with Session(engine) as session1:
#     if session1.query(models.Rol).count() == 0:
#         roles = [
#             models.Rol(nombre_rol='Administrador', descripcion='Rol con acceso total'),
#             models.Rol(nombre_rol='Estudiante', descripcion='Rol para estudiantes'),
#             models.Rol(nombre_rol='Asesor', descripcion='Rol para asesores'),
#             models.Rol(nombre_rol='Secretario', descripcion='Rol para secretarios')
#         ]
#         session1.add_all(roles)
#         session1.commit()
#         print("Datos por defecto insertados en la tabla Roles.")
#     else:
#         print("Los datos por defecto ya existen en la tabla Roles.")


# Dependencia para obtener la sesión
async def get_db():
    db = SessionLocal()
    try:
        yield db # Devuelve la sesión al contexto
    finally:
        db.close()  # Asegura que la sesión se cierre



########################################################

########################################################

@app.post("/roles/", tags=["Roles"])
async def crear_rol(rol: RolBase, db: Session = Depends(get_db)):
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
async def crear_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):
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
@app.get("/usuarios/{usuario_id}", response_model=UsuarioBase, tags=["Usuarios"])
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
@app.get("/usuarios/", response_model=List[UsuarioBase], tags=["Usuarios"])
async def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()  # Seleccionar todos los usuarios
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    
    return usuarios  # Retorna la lista de usuarios


@app.get("/tesistas_disponibles", response_model=List[UsuarioBase], tags=["Usuarios"])
async def obtener_tesistas(db: Session = Depends(get_db)):

    # Obbtener los IDs de usuarios que están en tesis
    subquery_tesis = db.query(
        models.Tesis.autor1.label("id_usuario")
    ).filter(models.Tesis.autor1.isnot(None))  # Filtrar NULL
    subquery_tesis = subquery_tesis.union_all(
        db.query(models.Tesis.autor2.label("id_usuario")).filter(models.Tesis.autor2.isnot(None)),  # Filtrar NULL
        db.query(models.Tesis.autor3.label("id_usuario")).filter(models.Tesis.autor3.isnot(None))  # Filtrar NULL
    ).distinct().subquery()  # Aseguramos que los IDs sean únicos

    # Obtener el ID del rol de Tesista
    tesista_rol_id = db.query(models.Rol.id_rol).filter(models.Rol.nombre_rol == 'Tesista').scalar()

    # Consulta principal para obtener los estudiantes que no estan en alguna tesis
    tesistas_disponibles = db.query(models.Usuario).filter(
        models.Usuario.id_rol == tesista_rol_id,
        models.Usuario.id_usuario.notin_(subquery_tesis)  # Filtramos los que están en la subconsulta
    ).all()

    if not tesistas_disponibles:
        raise HTTPException(status_code=404, detail="No se encontraron tesistas disponibles")

    # Convertir el resultado en una lista de diccionarios
    response = [
        {
            "id_usuario": tesista.id_usuario,
            "apellido_paterno": tesista.apellido_paterno,
            "apellido_materno": tesista.apellido_materno,
            "nombres": tesista.nombres,
            "grado_academico": tesista.grado_academico,
        }
        for tesista in tesistas_disponibles
    ]

    return JSONResponse(content=response)  # Devolver la respuesta en formato JSON


# Endpoint para obtener todos los usuarios
@app.get("/docentes", response_model=List[UsuarioBase], tags=["Usuarios"])
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
async def editar_usuario(usuario_id: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
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

@app.post("/propuestatesis/", tags=["PlanTesis"])
async def crear_propuestatesis(propuesta: TesisBase, db: Session = Depends(get_db)):
    db_propuesta = models.PropuestaTesis(
        titulo_tentativo=propuesta.titulo_tentativo,
        descripcion=propuesta.descripcion,
        keywords=propuesta.keywords,
        asesor=propuesta.asesor, 
        estado=propuesta.estado,
        path_tesis=propuesta.path_tesis, # Path de la tesis
        # fecha_inscripcion=propuesta.fecha_inscripcion,  # Fecha de inscripción, por defecto la actual
        # fecha_modificacion=propuesta.fecha_modificacion  # Fecha de modificación, por defecto la actual
    )
    # Validar que se esta agregando
    try:
        db.add(db_propuesta)
        db.commit()
        db.refresh(db_propuesta)
        return {
            'detail': 'Success',
        }
    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(status_code=500, detail=str(e))  # Retornar un error 500


#SUBIR ARCHIVO .txt
# @app.post('/files', tags=["PlanTesis"])
# def get_file(file: bytes = File(...)):
#     content = file.decode('utf-8')
#     lines = content.split('\n')
#     return {"content": lines}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

#Subir archivos, restringir a .PDF
@app.post('/upload_propuesta', tags=["PlanTesis"])
async def upload_file(uploaded_file: UploadFile = File(...)):
    # Verifica la extensión del archivo
    if not allowed_file(uploaded_file.filename):
        raise HTTPException(status_code=400, detail="Extensión de archivo no válida. Solo se admite .pdf")
    
    # Renombrar el archivo
    new_name = "01-PT-2024-2.pdf"
    path_d = "files/"+new_name
    
    # Guarda el archivo directamente en el destino
    with open(path_d, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    ## GUARDAR PATH DE PLAN DE TESIS

    return {
        'filename': uploaded_file.filename,
        'content_type': uploaded_file.content_type,
        'path': path_d,
        'detail': 'Success'
    }

@app.get("/propuestatesis/{propuesta_id}", tags=["PlanTesis"])
async def get_propuesta_by_id(id_tesis: int, db: Session = Depends(get_db)):
    propuesta = db.query(models.Tesis).filter(models.Tesis.id_tesis == id_tesis).first()
    if propuesta is None:
        raise HTTPException(status_code=404, detail="Propuesta de tesis no encontrada")
    return propuesta


# Lanzar configuracion automatica para ejecucion
# Para pruebas locales

#if __name__ == '__main__':
#    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
