from sqlalchemy.orm import Session
from sqlalchemy import text
from ..pymodels import models
from .database import SessionLocal
import os

# Ejecutar archivo SQL
def execute_sql_file(session: Session, file_path: str):
    try:
        full_path = os.path.join(os.path.dirname(__file__), 'sql', file_path)   
        # Leer el archivo SQL
        with open(full_path, 'r', encoding='utf-8') as file:
            sql = file.read()

        # Ejecutar el SQL
        session.execute(text(sql))

        # Hacer commit para asegurar que los cambios se guarden en la base de datos
        session.commit()
    
    except Exception as e:
        # Si hay un error, hacer rollback para revertir la transacción
        session.rollback()
        print(f"Error al ejecutar SQL: {e}")
 
# Inicializar datos por defecto
async def initialize_default_data():
    with SessionLocal() as session:
        # Uso de la función general para cada tabla
        insert_default_data(session, models.Rol, 'insert_default_roles.sql', 'rol')
        insert_default_data(session, models.Usuario, 'insert_default_users.sql', 'usuario')
        insert_default_data(session, models.Tesis, 'insert_default_tesis.sql', 'tesis')
        insert_default_data(session, models.NotificationEntity, 'insert_default_notifications_template.sql', 'notification_entities')
        session.commit()


def insert_default_data(session: Session, model, file_path: str, table_name: str):
    if session.query(model).count() == 0:
        execute_sql_file(session, file_path=file_path)
        print(f"Datos por defecto insertados en la tabla '{table_name}'.")
    else:
        print(f"Los datos por defecto ya existen en la tabla '{table_name}'.")


# def execute_sql_file(session, file_path):
#     # UTF para procesar informacion con tildes y caracteres en español
#     with open(file_path, 'r', encoding='utf-8') as file:
#         sql = file.read()
#     session.execute(text(sql))  # Usa text() para envolver la consulta SQL

# async def initialize_default_data():
#     """
#     Función para inicializar datos por defecto en la base de datos
#     """
#     with SessionLocal() as session:
#         await insert_default_roles(session)
#         await insert_default_users(session)
#         session.commit()
   
# async def insert_default_roles(session: Session):
#     """
#     Inserta roles por defecto si no existen
#     """
#     if session.query(models.Rol).count() == 0:
#         execute_sql_file(session, file_path='../insert_default_roles.sql')
#         print("Datos por defecto insertados en la tabla Roles.")
#     else:
#         print("Los datos por defecto ya existen en la tabla Roles.")
       
# async def insert_default_users(session: Session):
#     """
#     Inserta roles por defecto si no existen
#     """
#     if session.query(models.Usuario).count() == 0:
#         execute_sql_file(session, file_path='../insert_default_users.sql')
#         print("Datos por defecto insertados en la tabla Usuarios.")
#     else:
#         print("Los datos por defecto ya existen en la tabla Usuarios.") 