from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from ..pymodels.models import Usuario, Tesis, Rol, NotificationEntity, Notification, NotificationReceiver
from ..pymodels.schemas import TesisBase, TesisAgregarBase
from ._services import get_current_user_http
from ..db.database import db_dependency
from ._services import oauth
from fastapi import Request
from fastapi.responses import RedirectResponse, JSONResponse
import os

router = APIRouter(
    prefix='/tesis',
    tags=['tesis']
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

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_tesis(
    db: db_dependency,
    tesis: TesisAgregarBase,
    current_user: Usuario = Depends(get_current_user_http)  # Dependencia de la función get_current_user_http
):
    # Obtener los IDs de los usuarios involucrados (current_user, autor2, autor3)
    usuarios_ids = [current_user.id_usuario]
    # Agregar solo si autor2 o autor3 no son None
    if tesis.autor2 is not None:
        usuarios_ids.append(tesis.autor2)

    if tesis.autor3 is not None:
        usuarios_ids.append(tesis.autor3)

    asesor_id = [tesis.asesor]

    # Verificar activo, regiustro y Tesistas de los 3 interesados
    rol_verificado, mensaje_error = verificar_roles_usuarios_completos(db, usuarios_ids, "Tesista")
    if not rol_verificado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensaje_error
        )

    # Verificar si alguno de los tesistas ya está en otra tesis
    for usuario_id in usuarios_ids:
        if verificar_tesista_en_tesis(db, usuario_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El usuario {obtener_nombres_usuario(db, usuario_id)} ya está inscrito en otra tesis"
            )
    
    # Verificar activo, registro y Docente del asesor
    rol_verificado, mensaje_error = verificar_roles_usuarios_completos(db, asesor_id, "Docente")
    if not rol_verificado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensaje_error
        )

    # Crear el modelo de tesis si el usuario no está en otra tesis
    create_tesis_model = Tesis(
        titulo = tesis.titulo,
        resumen = tesis.resumen,
        especialidad = tesis.especialidad,
        keywords = tesis.keywords,
        autor1=current_user.id_usuario,
        autor2=tesis.autor2,
        autor3=tesis.autor3,
        asesor = tesis.asesor,
        actividad_focus = tesis.actividad_focus,
    )

    db.add(create_tesis_model)
    db.commit()

    #return {"message": "Tesis creado correctamente"}
    db.refresh(create_tesis_model)

    if len(usuarios_ids) > 1:
        # Crear notificaciones para los autores y el asesor
        for user_id in usuarios_ids[1:]:

            ######### NOTIFIACION PARA EL QUE INGRESA LA TESIS (INVITACION A OTROS AUTORES) ########
            # Recuperar la entidad de notificación para invitar a los autores
            inclusion_entity = db.query(NotificationEntity).filter_by(
                entity="propuesta_tesis",
                entity_kind="inclusión",
                type="tesista_invita"
            ).first()
            print(obtener_nombres_usuario(db,user_id))
            # Crear notificación para el que esta invitando
            new_notification = Notification(
                message=inclusion_entity.template.format(usuario_nombres=obtener_nombres_usuario(db,user_id)),
                notification_entity_id=inclusion_entity.id,
                actor_type="Tesista",
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
                actor_type="Tesista",
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
        message=propuesta_entity.template.format(usuario=current_user, tesis=tesis),
        notification_entity_id=propuesta_entity.id,
        actor_type="Docente",
        actor_id=tesis.asesor
    )
    db.add(asesor_notification)
    db.commit()
    db.refresh(asesor_notification)

    # Crear receptor de notificación para el asesor
    asesor_receiver = NotificationReceiver(
        notification_id=asesor_notification.id,
        user_id=tesis.asesor
    )
    db.add(asesor_receiver) 
    db.commit()

    return {"message": "Tesis creada correctamente y notificaciones enviadas"}