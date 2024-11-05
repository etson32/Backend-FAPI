from sqlalchemy.orm import Session
from sqlalchemy import text
import models
from database import SessionLocal
from sqlalchemy import text

# Ejecutar archivo SQL
def execute_sql_file(session: Session, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql = file.read()
    session.execute(text(sql))

# Inicializar datos por defecto
async def initialize_default_data():
    with SessionLocal() as session:
        await insert_default_roles(session)
        await insert_default_users(session)
        await insert_default_tesis(session)
        session.commit()

async def insert_default_roles(session: Session):
    if session.query(models.Rol).count() == 0:
        execute_sql_file(session, file_path='../insert_default_roles.sql')
        print("Datos por defecto insertados en la tabla 'rol'.")
    else:
        print("Los datos por defecto ya existen en la tabla 'rol'.")

async def insert_default_users(session: Session):
    if session.query(models.Usuario).count() == 0:
        execute_sql_file(session, file_path='../insert_default_users.sql')
        print("Datos por defecto insertados en la tabla 'usuario'.")
    else:
        print("Los datos por defecto ya existen en la tabla 'usuario'.")

async def insert_default_tesis(session: Session):
    if session.query(models.Tesis).count() == 0:
        execute_sql_file(session, file_path='../insert_default_tesis.sql')
        print("Datos por defecto insertados en la tabla 'tesis'.")
    else:
        print("Los datos por defecto ya existen en la tabla 'tesis'.")


 

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