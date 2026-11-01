import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SCHEMA_FILE = BASE_DIR / "sql" / "01_schema.sql"
INDEX_FILE = BASE_DIR / "sql" / "02_indexes.sql"

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
# CREATE TABLES
# ============================================================

schema_sql = SCHEMA_FILE.read_text(
    encoding="utf-8"
)

with conn.cursor() as cur:

    cur.execute(schema_sql)

conn.commit()

print("Database schema created.")

# ============================================================
# CLEAR EXISTING DATA
# ============================================================
with conn.cursor() as cur:
    cur.execute("""
        TRUNCATE TABLE
            fact_inventory_current,
            fact_sales,
            dim_product,
            dim_category,
            dim_date,
            dim_store
        RESTART IDENTITY CASCADE;
    """)

conn.commit()

print("Existing data cleared.")


# ============================================================
# LOAD CSV USING COPY
# ============================================================

tables = [
    (
        "dim_store",
        "dim_store.csv"
    ),
    (
        "dim_category",
        "dim_category.csv"
    ),
    (
        "dim_product",
        "dim_product.csv"
    ),
    (
        "dim_date",
        "dim_date.csv"
    ),
    (
        "fact_sales",
        "fact_sales.csv"
    ),
    (
        "fact_inventory_current",
        "fact_inventory_current.csv"
    ),
]


for table_name, filename in tables:

    file_path = (
        PROCESSED_DIR / filename
    )

    print(
        f"Loading {filename}..."
    )

    with conn.cursor() as cur:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            with cur.copy(
                f"""
                COPY {table_name}
                FROM STDIN
                WITH CSV HEADER
                """
            ) as copy:

                while data := file.read(1024 * 1024):

                    copy.write(data)

    conn.commit()

    print(
        f"{table_name}: loaded"
    )


# ============================================================
# CREATE INDEXES
# ============================================================

index_sql = INDEX_FILE.read_text(
    encoding="utf-8"
)

with conn.cursor() as cur:
    cur.execute(index_sql)

conn.commit()

print("Indexes created.")

conn.close()

print("\nDatabase loading completed.")
