from ..db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, ARRAY, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

class Tesis(Base):
    __tablename__ = 'tesis'

    id_tesis = Column(Integer, primary_key=True, autoincrement=True)  # Identificador de toda la tesis
    titulo = Column(String, nullable=False)  # Titulo de la tesis
    resumen = Column(String, nullable=False)  # Resumen o abstract de la tesis
    especialidad = Column(String, nullable=False)  # Especialidad de la carrera
    keywords = Column(ARRAY(String))  # Temas relacionados
    #autor1 = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)  # Autor 1
    #autor2 = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=True)  # Autor 2 (opcional)
    #autor3 = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=True)  # Autor 3 (opcional)
    #asesor = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)  # Asesor docente
    creacion_en = Column(DateTime, default=datetime.now)  # Fecha de creación de tesis
    actividad_focus = Column(String, nullable=False)  # Actividad actual
    #revisor1 = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=True)  # Revisor 1 (opcional)
    #revisor2 = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=True)  # Revisor 2 (opcional)
    asesorado = Column(Boolean, default=False)  # Estado de asesoramiento
    editado_en = Column(DateTime, onupdate=datetime.now)  # Última fecha de edición 
 
    # Relaciones
    #autor1_rel = relationship('Usuario', foreign_keys=[autor1])
    #autor2_rel = relationship('Usuario', foreign_keys=[autor2])
    #autor3_rel = relationship('Usuario', foreign_keys=[autor3])
    #asesor_rel = relationship('Usuario', foreign_keys=[asesor])
    #revisor1_rel = relationship('Usuario', foreign_keys=[revisor1])
    #revisor2_rel = relationship('Usuario', foreign_keys=[revisor2])
    #documentos = relationship('Documentos', back_populates='tesis')  # Relación con Documentos

class IntegrantesTesis(Base):
    __tablename__ = 'integrantes_tesis'

    id_int = Column(Integer, primary_key=True, autoincrement=True)  # Identificador de toda la tesis
    id_tesis = Column(Integer, ForeignKey('tesis.id_tesis'), nullable=False)  # id de la tesis
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=True)  # id_usuario
    id_rol = Column(Integer, ForeignKey('rol.id_rol'), nullable=True)  # Autor 3 (opcional)



class PlanTesis(Base): 
    __tablename__ = 'plan_tesis' 

    id_plan_tesis = Column(Integer, primary_key=True, autoincrement=True)  # Identificador del plan de tesis
    id_tesis = Column(Integer, ForeignKey('tesis.id_tesis'), nullable=False)  # Relación con la tabla Tesis
    estado = Column(Enum('Visto', 'Observado', 'Aprobado', 'Rechazado', name='estado_enum'), nullable=False)  # Estado del plan de tesis
    direccion_pdf = Column(String, nullable=False)  # Dirección del archivo PDF
    fecha_creacion = Column(DateTime, default=datetime.now)  # Fecha de creación del plan de tesis
    fecha_modificacion = Column(DateTime, nullable=True)  # Fecha de modificación del plan de tesis
    

class RevisarTesis(Base):
    __tablename__ = 'revisar_tesis'

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)  # Identificador del comentario
    id_plan_tesis = Column(Integer, ForeignKey('plan_tesis.id_plan_tesis'), unique= True, nullable=False)  # Relación con la tabla Plan_Tesis
    descripcion = Column(String, nullable=False)  # Descripción breve de las observaciones
    completado = Column(Boolean, default=False)  # Indica si el comentario ha sido completado
    fecha_creacion = Column(DateTime, default=datetime.now)  # Fecha de creación del comentario
    fecha_completado = Column(DateTime, nullable=True)  # Fecha de observación subsanada (opcional)
    origen_entidad = Column(Enum('Propuesta', 'Plan', name='origen_entidad_enum'), nullable=False)  # Origen del comentario


class Documentos(Base):
    __tablename__ = 'documentos'

    id_doc = Column(Integer, primary_key=True, autoincrement=True)  # Identificador de la actividad de generación
    id_tesis = Column(Integer, ForeignKey('tesis.id_tesis'), nullable=False)  # Relación con la tabla Tesis
    nombre_archivo = Column(String, nullable=False)  # Nombre del archivo
    detalle = Column(String, nullable=True)  # Detalles adicionales
    tipo = Column(Enum('Oficio', 'Resolucion', 'Proveido', 'Informe Turnitin', name='tipo_enum'), nullable=False)  # Tipo de documento
    create_by = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)  # ID del usuario que creó el documento
    create_at = Column(DateTime, default=datetime.now)  # Fecha de creación del documento
    update_at = Column(DateTime, nullable=True)  # Fecha de última modificación del documento
    fase = Column(String, nullable=True)  # Fase del proceso
    estado = Column(Enum('Activo', 'Inactivo', 'Rechazado', name='estado_enum'), default='Activo')  # Estado del documento
    direccion_url = Column(String, nullable=False)  # Dirección URL del documento

    #tesis = relationship('Tesis', back_populates='documentos')  # Relación inversa
    

# ===========================================================================#
# ===========================================================================#
# -------------------- USUARIOS ------------------- #	

class Notificacion(Base):
    __tablename__ = 'notificaciones'
    
    id = Column(String, primary_key=True)  # Identificador único de la notificación
    asunto = Column(String(255), nullable=False)  # Asunto de la notificación (tipo)
    tesis_id = Column(Integer, ForeignKey('tesis.id_tesis'), nullable=False)  # Relación con la tabla Tesis
    usuario_id = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)  # Relación con la tabla Usuario
    es_aceptado = Column(Boolean, default=False)  # Estado de la notificación (aceptado o no)
    creado_en = Column(DateTime, nullable=False)  # Fecha y hora de creación de la notificación
    respondido_en = Column(DateTime, nullable=True)  # Fecha y hora de respuesta (puede ser nulo)


# ===========================================================================#
# ===========================================================================#
# -------------------- CREDENCIALES DE SESION ------------------- #	

# ===========================================================================#
# ===========================================================================#
# -------------------- USUARIOS ------------------- #	

# Tabla de Roles
class Tipo(Base):
    __tablename__ = 'tipo'  
 
    id_tipo = Column(Integer, primary_key=True, autoincrement=True)  # Identificador único del tipo
    nombre_tipo = Column(String, nullable=False, unique=True)  # Nombre del rol (Ej.: Estudiante, Asesor, Secretario)
    descripcion = Column(String, nullable=True)  # Descripción de las responsabilidades de ese rol

    # Relación con Usuarios 
    #usuarios = relationship("Usuario", back_populates="rol")

class Rol(Base): 
    __tablename__ = 'rol' 
 
    id_rol = Column(Integer, primary_key=True, autoincrement=True)  # Identificador único del rol
    nombre_rol = Column(String, nullable=False, unique=True)  # Nombre del rol (Ej.: Estudiante, Asesor, Secretario)
    descripcion = Column(String, nullable=True)  # Descripción de las responsabilidades de ese rol  
   
# Tabla de Usuarios
class Usuario(Base): 
    __tablename__ = 'usuario'
 
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)  # Identificador único del usuario
    apellidos_familiar = Column(String, nullable=False)  # Apellido paterno del usuario
    nombres = Column(String, nullable=False)  # Nombres del usuario
    email = Column(String, nullable=False, unique=True)  # Correo electrónico usado para el login
    dni = Column(String, nullable=True, unique=True)  # Documento de identidad | Opcional
    password_hash = Column(String, nullable = False, default="unsaac")  # Contraseña cifrada para autenticación
    google_sub = Column(String, unique=True, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now)  # Fecha en que se creó la cuenta
    grado_academico = Column(String, nullable=False, default="Invitado") #  estudiante, bachiler, licenciado, ingeniero, abogado, magister, doctor, etc.
    ###NUEVA COLUMNA
    foto_perfil = Column(String, nullable=True)  # Foto de perfil del estudiante.
    activo = Column(Boolean, default=False)  # Indica si el usuario está activo o inactivo
    esta_registrado = Column(Boolean, default=False)  # Indica si el usuario está activo o inactivo
    id_tipo = Column(Integer, ForeignKey('tipo.id_tipo'), nullable=False, default=3)  # Relación con la tabla Roles invitado por defecto
     
    # Relación con Rol
    #rol = relationship("Rol", back_populates="Usuario")

 
# Tabla de Permisos
class Permiso(Base):
    __tablename__ = 'permisos'

    id_permiso = Column(Integer, primary_key=True, autoincrement=True)  # Identificador único del permiso
    nombre_permiso = Column(String, nullable=False, unique=True)  # Nombre del permiso (Ej.: Crear Propuesta, Revisar Plan)
    descripcion = Column(String, nullable=True)  # Descripción del permiso


# Tabla de Rol_Permiso (relación muchos a muchos entre Roles y Permisos)
class RolPermiso(Base):
    __tablename__ = 'rol_permiso'

    id_rol_permiso = Column(Integer, primary_key=True, autoincrement=True)  # Identificador único de la relación
    id_rol = Column(Integer, ForeignKey('rol.id_rol'), nullable=False)  # Referencia al identificador del rol
    id_permiso = Column(Integer, ForeignKey('permisos.id_permiso'), nullable=False)  # Referencia al identificador del permiso
    fecha_asignacion = Column(DateTime, default=datetime.now)  # Fecha en que se asignó el permiso al rol


# ===========================================================================#
# ===========================================================================#
# -------------------- NOTIFICACIONES ------------------- #	

# Enum de Python
class NotificationType(PyEnum):
    PROPUESTA_ENVIADA = "propuesta_enviada" # Asesor es notificado para aceptar propuesta de tesis
    PROPUESTA_ACEPTADA = "propuesta_aceptada" # Asesor acepta propuesta de tesis
    INVITACION_USUARIO = "invitacion_usuario" # Tesista agrega a autor 2 o 3 
    CORRECCION_REQUERIDA = "correccion_requerida" # Asesor envia sugerencias de correccion tesis

class NotificationEntity(Base):
    __tablename__ = "notification_entities"
 
    id = Column(Integer, primary_key=True)
    entity = Column(String, nullable=False)  # Por ejemplo, 'tesis'
    entity_kind = Column(String, nullable=False)  # Tipo de notificación (e.g., 'inclusión', 'corrección')
    type = Column(String, nullable=False)  # Por ejemplo, 'tesis'
    template = Column(String, nullable=False) 
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now())

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    notification_entity_id = Column(Integer, ForeignKey("notification_entities.id"), nullable=False)
    actor_type = Column(String, nullable=True)  # Por ejemplo, 'Asesor' o 'Estudiante'
    actor_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now())

class NotificationReceiver(Base):
    __tablename__ = "notification_receivers"

    id = Column(Integer, primary_key=True)
    notification_id = Column(Integer, ForeignKey("notifications.id"), nullable=False)
    notification = relationship("Notification")
    user_id = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    read_status = Column(Boolean, default=False)
    date_read = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)