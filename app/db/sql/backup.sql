--
-- PostgreSQL database dump
--

CREATE TABLE public."Carta_Aceptacion" (
    id_carta integer NOT NULL,
    id_plan_tesis integer NOT NULL,
    direccion_pdf character varying NOT NULL,
    fecha_creacion timestamp without time zone,
    fecha_modificacion timestamp without time zone
);


CREATE TABLE public."Informe_Turnitin" (
    id_inf_turnitin integer NOT NULL,
    id_plan_tesis integer NOT NULL,
    porcentaje_similitud double precision NOT NULL,
    direccion_pdf character varying NOT NULL,
    fecha_creacion timestamp without time zone,
    fecha_modificacion timestamp without time zone
);


CREATE TABLE public."PTesis_Observaciones" (
    id_observaciones integer NOT NULL,
    id_plan_tesis integer NOT NULL,
    descripcion text NOT NULL,
    completado boolean NOT NULL,
    fecha_creacion timestamp without time zone,
    fecha_completado timestamp without time zone
);

CREATE TABLE public."Permisos" (
    id_permiso integer NOT NULL,
    nombre_permiso character varying NOT NULL,
    descripcion character varying
);


CREATE TABLE public."Plan_Tesis" (
    id_plan_tesis integer NOT NULL,
    id_propuesta integer NOT NULL,
    titulo character varying NOT NULL,
    descripcion text NOT NULL,
    especialidad character varying NOT NULL,
    keywords character varying[] NOT NULL,
    estado character varying NOT NULL,
    id_usuario_tesista1 integer NOT NULL,
    id_usuario_tesista2 integer,
    id_usuario_asesor integer NOT NULL,
    direccion_pdf character varying NOT NULL,
    fecha_creacion timestamp without time zone,
    fecha_modificacion timestamp without time zone
);



CREATE TABLE public."Propuesta_Observaciones" (
    id_comentario integer NOT NULL,
    id_propuesta integer NOT NULL,
    descripcion text NOT NULL,
    completado boolean NOT NULL,
    fecha_creacion timestamp without time zone,
    fecha_completado timestamp without time zone,
    origen_entidad character varying NOT NULL
);



CREATE TABLE public."Propuesta_Tesis" (
    id_propuesta integer NOT NULL,
    titulo character varying NOT NULL,
    descripcion text NOT NULL,
    especialidad character varying NOT NULL,
    keywords character varying[] NOT NULL,
    estado character varying NOT NULL,
    id_usuario_tesista1 integer NOT NULL,
    id_usuario_tesista2 integer,
    id_usuario_asesor integer NOT NULL,
    fecha_generacion timestamp without time zone,
    fecha_modificacion timestamp without time zone
);


CREATE TABLE public."Rol_Permiso" (
    id_rol_permiso integer NOT NULL,
    id_rol integer NOT NULL,
    id_permiso integer NOT NULL,
    fecha_asignacion timestamp without time zone
);



CREATE TABLE public."Roles" (
    id_rol integer NOT NULL,
    nombre_rol character varying NOT NULL,
    descripcion character varying
);



CREATE TABLE public."TramiteF1" (
    id_tramite integer NOT NULL,
    id_plan_tesis integer NOT NULL,
    nro_tramite character varying NOT NULL,
    estado character varying NOT NULL,
    detalle character varying NOT NULL,
    fecha_tramite timestamp without time zone,
    fecha_recibe_secretario timestamp without time zone
);


CREATE TABLE public."Usuario" (
    id_usuario integer NOT NULL,
    apellido_paterno character varying NOT NULL,
    apellido_materno character varying NOT NULL,
    nombres character varying NOT NULL,
    correo_electronico character varying NOT NULL,
    dni character varying NOT NULL,
    password_hash character varying NOT NULL,
    fecha_creacion timestamp without time zone,
    activo boolean,
    id_rol integer NOT NULL
);

