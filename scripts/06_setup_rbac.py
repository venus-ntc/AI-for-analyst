import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SQL_FILE = BASE_DIR / "sql" / "04_rbac_rls.sql"


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = psycopg.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    dbname=os.getenv("PG_DATABASE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")
)


print("Connected to PostgreSQL.")


# ============================================================
# EXECUTE RBAC SQL
# ============================================================

try:

    sql = SQL_FILE.read_text(
        encoding="utf-8"
    )

    with conn.cursor() as cur:

        cur.execute(sql)

    conn.commit()

    print("RBAC configuration completed.")

finally:

    conn.close()

    print("Database connection closed.")
