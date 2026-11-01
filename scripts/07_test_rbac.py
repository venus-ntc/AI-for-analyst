import os

import psycopg
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


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


try:

    with conn.cursor() as cur:

        # ====================================================
        # 1. Check application role
        # ====================================================

        cur.execute("""
            SELECT
                rolname,
                rolsuper,
                rolbypassrls
            FROM pg_roles
            WHERE rolname = 'retail_app';
        """)

        print("\nApplication role:")
        print(cur.fetchone())


        # ====================================================
        # 2. Switch to application role
        # ====================================================

        cur.execute("""
            SET ROLE retail_app;
        """)

        cur.execute("""
            SELECT
                current_user,
                session_user;
        """)

        print("\nAfter SET ROLE:")
        print(cur.fetchone())


        # ====================================================
        # 3. Set application user context
        #
        # user_id = 1 = van
        # ====================================================

        cur.execute("""
            SELECT set_config(
                'app.user_id',
                '1',
                true
            );
        """)

        print("\nApplication user context:")
        print("user_id = 1 (van)")


        # ====================================================
        # 4. Check RLS status
        # ====================================================

        cur.execute("""
            SELECT
                relname,
                relrowsecurity
            FROM pg_class
            WHERE relname = 'fact_sales';
        """)

        print("\nRLS status:")
        print(cur.fetchone())


        # ====================================================
        # 5. Count visible rows
        # ====================================================

        cur.execute("""
            SELECT COUNT(*)
            FROM fact_sales;
        """)

        visible_rows = cur.fetchone()[0]

        print("\nVisible fact_sales rows:")
        print(visible_rows)


        # ====================================================
        # 6. Check visible store IDs
        # ====================================================

        cur.execute("""
            SELECT DISTINCT store_id
            FROM fact_sales
            ORDER BY store_id;
        """)

        store_ids = [row[0] for row in cur.fetchall()]

        print("\nVisible store IDs:")
        print(store_ids)


        # ====================================================
        # 7. Check unauthorized stores
        # ====================================================

        cur.execute("""
            SELECT COUNT(*)
            FROM fact_sales
            WHERE store_id NOT IN (1, 2, 3);
        """)

        unauthorized_rows = cur.fetchone()[0]

        print("\nUnauthorized rows:")
        print(unauthorized_rows)


finally:

    conn.close()

    print("\nDatabase connection closed.")
