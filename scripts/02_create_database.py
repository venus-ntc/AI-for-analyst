import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

admin_db = os.getenv("PG_ADMIN_DB")
target_db = os.getenv("PG_DATABASE")

conn = psycopg.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    dbname=admin_db,
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    autocommit=True
)

with conn.cursor() as cur:

    cur.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s;",
        (target_db,)
    )

    exists = cur.fetchone()

    if exists:
        print(f"Database '{target_db}' already exists.")
    else:
        cur.execute(
            f'CREATE DATABASE "{target_db}";'
        )
        print(f"Database '{target_db}' created.")

conn.close()
