import os
import psycopg

from dotenv import load_dotenv


load_dotenv()


conn = psycopg.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    dbname=os.getenv("PG_DATABASE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")
)


tables = [
    "dim_store",
    "dim_category",
    "dim_product",
    "dim_date",
    "fact_sales",
    "fact_inventory_current"
]


with conn.cursor() as cur:

    for table in tables:

        cur.execute(
            f"SELECT COUNT(*) FROM {table};"
        )

        count = cur.fetchone()[0]

        print(
            f"{table:30} {count:,}"
        )


conn.close()

