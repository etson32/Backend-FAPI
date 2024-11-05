from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

# url_object = URL.create(
#     "postgresql",
#     username="postgres",
#     password="123",  # plain (unescaped) text
#     host="localhost",
#     database="SCT",
# )

#URL_DB = "postgresql://postgres:123@localhost:5432/SControlTesis"


# # Crear la conexión con la base de datos
# engine = create_engine(URL_DB)
# SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

# # Modelo base para crear tablas
# Base = declarative_base()
 

# Configuración de conexión
# username = 'postgres'
# password = '123'
# host = 'localhost'
# port = '5432'
# new_database_name = 'SControlTesis'

# # Configurar la URL de conexión a PostgreSQL
# DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/postgres'

# try:
#     # Conexión a la base de datos 'postgres'
#     conn = psycopg2.connect(DATABASE_URL)
#     conn.autocommit = True  # Habilitar autocommit

#     with conn.cursor() as cursor:
#         # Verificar si la base de datos ya existe
#         check_db_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{new_database_name}';"
#         cursor.execute(check_db_query)
#         exists = cursor.fetchone()
 
#         if not exists:
#             # Ejecutar CREATE DATABASE
#             create_db_query = f'CREATE DATABASE "{new_database_name}" WITH ENCODING = \'UTF8\';'
#             cursor.execute(create_db_query)
#             print(f"Base de datos '{new_database_name}' creada exitosamente.")
#         else:
#             print(f"La base de datos '{new_database_name}' ya existe. Conectando...")

#     conn.close()  # Cerrar la conexión

# except Exception as e:
#     print(f"Ocurrió un error al intentar crear a la base de datos: {e}")
  
# Crear un nuevo motor para la nueva base de datos
#Para pruebas locales
#new_database_url = f'postgresql://{username}:{password}@{host}:{port}/{new_database_name}?client_encoding=UTF8'

#Para deploy
new_database_url = 'postgresql://unsaac:7H1nGw7xiHdOqOPOaBjERfV5dV1A8Tvc@dpg-csl48go8fa8c73e05d30-a/scontroltesis'

# Crear el motor y la sesión
engine = create_engine(new_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base para los modelos
Base = declarative_base()




