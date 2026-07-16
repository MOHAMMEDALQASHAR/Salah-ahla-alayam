import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

try:
    # Connect to default postgres database to create the new database
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE ahla_alayam')
    cursor.close()
    conn.close()
    print("Database ahla_alayam created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print("Database ahla_alayam already exists.")
except Exception as e:
    print(f"Error creating database (check postgres credentials): {e}")
