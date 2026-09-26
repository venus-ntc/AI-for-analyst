## -------- test khi cài đặt postgres
# import os
# import psycopg
# from dotenv import load_dotenv

# load_dotenv()

# conn = psycopg.connect(
#     host=os.getenv("PG_HOST"),
#     port=os.getenv("PG_PORT"),
#     dbname=os.getenv("PG_ADMIN_DB"),
#     user=os.getenv("PG_USER"),
#     password=os.getenv("PG_PASSWORD")
# )

# print("PostgreSQL connection: OK")

# with conn.cursor() as cur:
#     cur.execute("SELECT version();")
#     version = cur.fetchone()[0]

#     print("PostgreSQL:")
#     print(version)

# conn.close()

##----------- test sau khi tạo database
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

print("PostgreSQL connection: OK")

with conn.cursor() as cur:
    cur.execute("SELECT current_database();")
    database = cur.fetchone()[0]

    cur.execute("SELECT current_user;")
    user = cur.fetchone()[0]

print("Database:", database)
print("User:", user)

conn.close()
