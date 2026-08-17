import os
from sqlalchemy import create_engine

MYSQL_USER = 'admin'
MYSQL_PASSWORD = 'adminpass123' 
MYSQL_DATABASE = 'tes_mysql'
MYSQL_PORT = '3306'
MYSQL_HOST = 'localhost'

mysql_engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")

PG_USER = 'postgres'
PG_PASSWORD = 'adminpass123'
PG_DATABASE = 'tes_postgres'
PG_PORT = '5432'
PG_HOST = 'localhost'

pg_engine = create_engine(f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}")
