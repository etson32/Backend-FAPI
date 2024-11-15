from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

# Agregar datos por defecto
class TesisBase(BaseModel):
    titulo: str  # Título de la tesis
    resumen: str  # Resumen o abstract de la tesis
    especialidad: str  # Especialidad de la carrera
    keywords: Optional[List[str]] = None   # Temas relacionados
    autor1: int  # ID del primer autor
    autor2: Optional[int] = None  # ID del segundo autor (opcional)
    autor3: Optional[int] = None  # ID del tercer autor (opcional)
    asesor: int  # ID del asesor
    actividad_focus: str  # Actividad actual de la tesis
    editado_en: Optional[datetime] = None  # Fecha de última edición

  # Agregar datos por defecto
class TesisAgregarBase(BaseModel):
    titulo: str  # Título de la tesis
    resumen: str  # Resumen o abstract de la tesis
    especialidad: str  # Especialidad de la carrera
    keywords: Optional[List[str]] = None   # Temas relacionados
    autor2: Optional[int] = None  # ID del segundo autor (opcional)
    autor3: Optional[int] = None  # ID del tercer autor (opcional) 
    asesor: int  # ID del asesor
    actividad_focus: str  # Actividad actual de la tesis 
    #editado_en: Optional[datetime] = None  # Fecha de última edición   

    # Si editado_en no es proporcionado, se asigna la fecha y hora actual
    @classmethod
    def set_default_editado_en(cls, values):
        if values.get('editado_en') is None: 
            values['editado_en'] = datetime.now()  # Asigna la fecha y hora actual
        return values

    class Config:
        from_atributes = True
        # Configurar el método de validación adicional para el campo editado_en
        @classmethod
        def validate(cls, values):
            return cls.set_default_editado_en(values)


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
    apellidos_familiar: str  # Apellido paterno del usuario
    nombres: str  # Nombres del usuario
    correo_electronico: str  # Correo electrónico usado para el login
    dni: str  # Documento de identidad
    password_hash: str  # Contraseña cifrada para autenticación
    google_sub: str # Acceso de google
    grado_academico : str # Grado academico de usuario
    activo: bool = False  # Indica si el usuario está activo o inactivo
    esta_registrado: bool = False
    id_rol: int  # Relación con la tabla Roles

class PermisoBase(BaseModel):
    nombre_permiso: str  # Nombre del permiso (Ej.: Crear Propuesta, Revisar Plan)
    descripcion: Optional[str] = None  # Descripción del permiso 

class RolPermisoBase(BaseModel):
    id_rol: int  # Referencia al identificador del rol
    id_permiso: int  # Referencia al identificador del permiso
    # fecha_asignacion: datetime  # Fecha en que se asignó el permiso al rol


####################################################################################################
###                                                                                              ###
### Definición de las clases para AUTORIZAR ingreso                                              ###
### Clases y funciones encargadas de gestionar el inicio de sesión y la verificación de permisos ###
###                                                                                              ###
####################################################################################################

class CreateUserRequestBase(BaseModel):
    #username: str
    password: str

class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class GoogleUserBase(BaseModel):
    sub: int
    email: str
    name: str
    picture: str

class RefreshTokenRequestBase(BaseModel):
    refresh_token: str

####################################################################################################
###                                                                                              ###
### Definición de las clases para VALIDAR ingreso                                                ###
### Clases y funciones encargadas de gestionar el inicio de sesión y la verificación de permisos ###
###                                                                                              ###
####################################################################################################

class CreateUserRequestBase(BaseModel):
    #email: str
    password: str

class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class GoogleUserBase(BaseModel):
    sub: int
    email: str
    name: str
    given_name: str
    family_name: str
    picture: str

class RefreshTokenRequestBase(BaseModel):
    refresh_token: str


# Definición del modelo de datos para la actualización de datos del usuario
class UpdateUserRequestBase(BaseModel):
    password: constr(min_length=8)  # Contraseña con una longitud mínima de 8 caracteres
    dni: int  # DNI 
    grado_academico: str  # Grado académico 
    id_rol: int  # Rol


