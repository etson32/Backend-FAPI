from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from typing import Annotated, List
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from ..pymodels.models import Usuario, Tesis, Rol, NotificationEntity, Notification, NotificationReceiver, IntegrantesTesis, Tipo
from ..pymodels.schemas import TesisBase, TesisAgregarBase, UsuarioBase, Usuario_FrontBase
from ._services import get_current_user_http
from ..db.database import db_dependency
from ._services import oauth
from fastapi import Request
from fastapi.responses import RedirectResponse, JSONResponse
import os

router = APIRouter(
    prefix='/notification',
    tags=['notification']
)

def obtener_nombres_usuario(db, usuario_id):
    usuario_tmp : Usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    return usuario_tmp.nombres+' '+usuario_tmp.apellidos_familiar

def verificar_tesista_en_tesis(db, usuario_id):
    tesis_existente = db.query(Tesis).filter((Tesis.autor1 == usuario_id) | (Tesis.autor2 == usuario_id) | (Tesis.autor3 == usuario_id)).first()
    return tesis_existente is not None

# Verificar si el usuario existe
def verificar_usuario_existe(db, usuario_id):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    return usuario if usuario else None, "El usuario no existe" if not usuario else None

# Verificar que el usuario tenga el rol especificado
def verificar_rol_usuario(db, usuario, rol_nombre):
    rol = db.query(Rol).filter(Rol.id_rol == usuario.id_rol, Rol.nombre_rol == rol_nombre).first()
    return rol is not None, f"El rol del usuario no corresponde a {rol_nombre}" if not rol else None

# Verificar que el usuario esté registrado
def verificar_usuario_registrado(usuario):
    return usuario.esta_registrado, "El usuario no está registrado" if not usuario.esta_registrado else None

# Verificar que el usuario esté activo
def verificar_usuario_activo(usuario):
    return usuario.activo, "El usuario no está activo" if not usuario.activo else None

# Función principal que combina todas las verificaciones para cualquier rol
def verificar_usuario_completo(db, usuario_id, rol_nombre):
    # Verificar que el usuario exista
    usuario, error = verificar_usuario_existe(db, usuario_id)
    if error:
        return False, error

    # Verificar que el usuario tenga el rol adecuado
    rol_valido, error = verificar_rol_usuario(db, usuario, rol_nombre)
    if error:
        return False, error

    # Verificar que el usuario esté registrado
    registrado, error = verificar_usuario_registrado(usuario)
    if error:
        return False, error

    # Verificar que el usuario esté activo
    activo, error = verificar_usuario_activo(usuario)
    if error:
        return False, error

    # Si todas las verificaciones se cumplen
    return True, f"Usuario verificado como {rol_nombre} registrado y activo"

# Función para verificar múltiples usuarios
def verificar_roles_usuarios_completos(db, usuarios_ids, rol_nombre):
    for usuario_id in usuarios_ids:
        rol_verificado, mensaje_error = verificar_usuario_completo(db, usuario_id, rol_nombre)
        if not rol_verificado:
            return False, f"Error con el usuario {obtener_nombres_usuario(db,usuario_id)}: {mensaje_error}"
    return True, None



@router.get("/tesistas_disponibles", response_model=List[Usuario_FrontBase])
async def tesistas_disponibles(db: db_dependency, current_user: Usuario = Depends(get_current_user_http)):

    if current_user.esta_registrado == False:
        raise HTTPException(status_code=404, detail="Este usuario no puede utilizar este endpoint")
    # Subconsulta: Usuarios en la tabla integrantes_tesis
    subquery_integrantes = db.query(IntegrantesTesis.id_usuario).subquery()

    # Consulta principal: Usuarios tipo "Investigador" que no están en la tabla integrantes_tesis
    tesistas_disponibles = db.query(Usuario, Tipo.nombre_tipo).join(
        Tipo, Tipo.id_tipo == Usuario.id_tipo  # Hacemos el JOIN con la tabla Tipo
    ).filter(
        Usuario.id_tipo == 2,  # Tipo 2 representa "Investigador"
        Usuario.esta_registrado == True,  # El usuario debe estar registrado
        Usuario.activo == True,  # El usuario debe estar activo
        ~Usuario.id_usuario.in_(subquery_integrantes.select()),  # NOT IN subquery
        Usuario.id_usuario != current_user.id_usuario # Excluir al usuario que hace la consulta
    ).all()

    # Si no hay tesistas disponibles, devolver error 404
    if not tesistas_disponibles:
        raise HTTPException(status_code=404, detail="No se encontraron tesistas disponibles.")

    # Convertir el resultado en una lista de diccionarios con solo los campos que deseas
    response = [
        Usuario_FrontBase(
            id=str(tesista.id_usuario),
            dni=tesista.dni,
            nombres=tesista.nombres,
            apellidos=tesista.apellidos_familiar,
            email=tesista.email, 
            tipo=tipo,  # nombre_tipo
            grado=tesista.grado_academico
        )
        for tesista, tipo in tesistas_disponibles  # Desempaquetamos la tupla (tesista, tipo)
    ]
 
    return response


@router.get("/docentes_disponibles", response_model=List[Usuario_FrontBase])
async def docentes_disponibles(db: db_dependency, current_user: Usuario = Depends(get_current_user_http)):

    if current_user.esta_registrado == False:
        raise HTTPException(status_code=404, detail="Este usuario no puede utilizar este endpoint")
    

    # Consulta principal: Usuarios tipo "Docente" que están registrados, activos, y no están en la tabla integrantes_tesis
    docentes_disponibles = db.query(Usuario, Tipo.nombre_tipo).join(
        Tipo, Tipo.id_tipo == Usuario.id_tipo  # Hacemos el JOIN con la tabla Tipo
    ).filter(
        Usuario.id_tipo == 3,  # Tipo 3 representa "Docente"
        Usuario.esta_registrado == True,  # El usuario debe estar registrado
        Usuario.activo == True,  # El usuario debe estar activo
    ).all()

    # Si no hay docentes disponibles, devolver error 404
    if not docentes_disponibles:
        raise HTTPException(status_code=404, detail="No se encontraron docentes disponibles.")

    # Convertir el resultado en una lista de diccionarios con solo los campos que deseas
    response = [
        Usuario_FrontBase(
            id=str(docente.id_usuario),
            dni=docente.dni,
            nombres=docente.nombres,
            apellidos=docente.apellidos_familiar,
            email=docente.email, 
            tipo=tipo,  # nombre_tipo
            grado=docente.grado_academico
        )
        for docente, tipo in docentes_disponibles  # Desempaquetamos la tupla (docente, tipo)
    ]
 
    return response


def validar_usuario(db, usuario_id: int):

    # Obtener el usuario desde la base de datos
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    # Verificar si el usuario existe
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario no encontrado: {usuario_id}.")
    
    # Verificar si el usuario está registrado
    if not usuario.esta_registrado:
        raise HTTPException(status_code=400, detail=f"El usuario {usuario.nombres} {usuario.apellidos_familiar} no está registrado.")
    
    # Verificar si el usuario está activo
    if not usuario.activo:
        raise HTTPException(status_code=400, detail=f"El usuario {usuario.nombres} {usuario.apellidos_familiar} no está activo.")
    
    # Si todo está bien, no hacer nada (deja continuar la ejecución)
    return None


def validar_investigador(db, usuario_id: int):
    # Verificar si el usuario ya está en la tabla integrantes_tesis
    usuario_en_tesis = db.query(IntegrantesTesis).filter(IntegrantesTesis.id_usuario == usuario_id).first()
    
    if usuario_en_tesis:
        raise HTTPException(status_code=400, detail=f"El usuario {obtener_nombres_usuario(db,usuario_en_tesis.id_usuario)} ya está en una tesis.")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_tesis(
    db: db_dependency,
    tesis: TesisAgregarBase,
    current_user: Usuario = Depends(get_current_user_http)  # Dependencia de la función get_current_user_http
): 

    # Recuperar id de los integrantes de tesis
    autores_ids = [current_user.id_usuario] + [
        autor_id for autor_id in [tesis.autor2, tesis.autor3] if autor_id is not None
    ]
    
    # Validar su estado activo y registrado
    for usuario_id in autores_ids:
        validar_usuario(db, usuario_id) 
        validar_investigador(db, usuario_id)
    if tesis.asesor is None:
        raise HTTPException(status_code=400, detail=f"No se tiene seleccionado un asesor.")
    validar_usuario(db, tesis.asesor)  

    #db.begin()
    # Crear el modelo de tesis si el usuario no está en otra tesis
    create_tesis_model = Tesis(
        titulo = tesis.titulo,
        resumen = tesis.resumen,
        especialidad = tesis.especialidad,
        keywords = tesis.keywords,
        #autor1=current_user.id_usuario,
        #autor2=tesis.autor2,
        #autor3=tesis.autor3,
        #asesor = tesis.asesor,
        actividad_focus = tesis.actividad_focus,
    )

    db.add(create_tesis_model)
    db.flush() # Solo hacemos flush para obtener el ID de la tesis

    for usuario_id in autores_ids:
        if usuario_id is not None:
            integrante_tesis = IntegrantesTesis(
                id_usuario=usuario_id,
                id_tesis=create_tesis_model.id_tesis,  # Usamos el ID de la tesis recién creada
                id_rol=1  # El rol de autor
            )
            db.add(integrante_tesis)
    integrante_tesis = IntegrantesTesis(
        id_usuario=tesis.asesor,
        id_tesis=create_tesis_model.id_tesis,  # Usamos el ID de la tesis recién creada
        id_rol=2  # El rol de asesor
    )
    db.add(integrante_tesis)
    db.commit()


    # AÑADIR NOTIFICACIONES
    for user_id in autores_ids:

        ######### NOTIFIACION PARA EL QUE INGRESA LA TESIS (INVITACION A OTROS AUTORES) ########
        # Recuperar la entidad de notificación para invitar a los autores
        inclusion_entity = db.query(NotificationEntity).filter_by(
            entity="propuesta_tesis",
            entity_kind="inclusión",
            type="tesista_invita"
        ).first()
        # Crear notificación para el que esta invitando
        new_notification = Notification(
            message=inclusion_entity.template.format(usuario_nombres=obtener_nombres_usuario(db,user_id)),
            notification_entity_id=inclusion_entity.id,
            actor_type="Investigador",
            actor_id=user_id
        )
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)

        # Crear receptor de notificación para cada autor
        notification_receiver = NotificationReceiver(
            notification_id=new_notification.id,
            user_id=user_id
        )
        db.add(notification_receiver)
        db.commit()

        ######### NOTIFICAR A AUTORES INVITADOS ########

        # Recuperar la entidad de notificación para invitar a los autores
        inclusion_entity = db.query(NotificationEntity).filter_by(
            entity="propuesta_tesis",
            entity_kind="inclusión",
            type="tesista_invitado"
        ).first()

        # Crear notificación para cada autor
        new_notification = Notification(
            message=inclusion_entity.template.format(usuario_nombres=obtener_nombres_usuario(db,user_id), tesis_titulo=tesis.titulo),
            notification_entity_id=inclusion_entity.id,
            actor_type="Investigador",
            actor_id=user_id
        )
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)

        # Crear receptor de notificación para cada autor
        notification_receiver = NotificationReceiver(
            notification_id=new_notification.id,
            user_id=user_id
        )
        db.add(notification_receiver)
        db.commit()

    # Crear notificación para el asesor al enviar la propuesta
    propuesta_entity = db.query(NotificationEntity).filter_by(
        entity="propuesta_tesis",
        entity_kind="propuesta",
        type="propuesta_enviada" 
    ).first()

    asesor_notification = Notification(
        message=propuesta_entity.template.format(usuario_nombres=obtener_nombres_usuario(db,user_id), tesis_titulo=tesis.titulo),
        notification_entity_id=propuesta_entity.id,
        actor_type="Docente",
        actor_id=tesis.asesor 
    )
    db.add(asesor_notification)
    db.commit()
    db.refresh(asesor_notification)

    # Crear receptor de notificación para el as esor
    asesor_receiver = NotificationReceiver(
        notification_id=asesor_notification.id,
        user_id=tesis.asesor 
    )
    db.add(asesor_receiver) 
    db.commit() 

    return {"message": "Tesis creada correctamente y notificaciones enviadas"}


# @router.get("/tesistas_disponibles", response_model=List[UsuarioBase])
# async def obtener_tesistas_disponibles( db: db_dependency,
#     current_user: Usuario = Depends(get_current_user_http)  # Dependencia de la función get_current_user_http
# ):

#     # Subconsulta: Usuarios en la tabla integrantes_tesis
#     subquery_integrantes = db.query(IntegrantesTesis.id_usuario).subquery()

#     # Consulta principal: Usuarios tipo "Investigador" que no están en la tabla integrantes_tesis
#     tesistas_disponibles = db.query(Usuario).filter(
#         Usuario.id_tipo == 2,  # Tipo 2 representa "Investigador"
#         ~Usuario.id_usuario.in_(subquery_integrantes)  # NOT IN subquery
#     ).all()

#     # Si no hay tesistas disponibles, devolver error 404
#     if not tesistas_disponibles:
#         raise HTTPException(status_code=404, detail="No se encontraron tesistas disponibles.")

#     # Retornar el resultado con el esquema definido
#     return tesistas_disponibles

