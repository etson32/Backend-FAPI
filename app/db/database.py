from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends
import psycopg2

# Se crea una base de datos si no se tiene aun, o se quiere reiniciar para hacer pruebas desde cero
# Base de datos local
username = 'postgres'
password = '123'
host = 'localhost'
port = '5432'
new_database_name = 'scontroltesis'

# Configurar la URL de conexión a PostgreSQL
DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/postgres'

try:
    # Conexión a la base de datos 'postgres'
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Habilitar autocommit

    with conn.cursor() as cursor:
        # Verificar si la base de datos ya existe
        check_db_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{new_database_name}';"
        cursor.execute(check_db_query)
        exists = cursor.fetchone()
 
        if not exists:
            # Ejecutar CREATE DATABASE
            create_db_query = f'CREATE DATABASE "{new_database_name}" WITH ENCODING = \'UTF8\';'
            cursor.execute(create_db_query)
            print(f"Base de datos '{new_database_name}' creada exitosamente.")
        else:
            print(f"La base de datos '{new_database_name}' ya existe. Conectando...")

    conn.close()  # Cerrar la conexión

except Exception as e:
    print(f"Ocurrió un error al intentar crear a la base de datos: {e}")
  
# Crear un nuevo motor para la nueva base de datos
#Para pruebas locales
new_database_url = f'postgresql://{username}:{password}@{host}:{port}/{new_database_name}?client_encoding=UTF8'

#Para deploy
#new_database_url = 'postgresql://unsaac:7H1nGw7xiHdOqOPOaBjERfV5dV1A8Tvc@dpg-csl48go8fa8c73e05d30-a/scontroltesis'

# Crear el motor y la sesión
engine = create_engine(new_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db # Devuelve la sesión al contexto
    finally:
        db.close()  # Asegura que la sesión se cierre

# Abrir sesion para cada endpoint
db_dependency = Annotated[Session, Depends(get_db)] 