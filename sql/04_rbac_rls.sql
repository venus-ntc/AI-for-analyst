-- ============================================================
-- RBAC BASE CONFIGURATION
-- ============================================================

-- 1. Create application roles
CREATE TABLE IF NOT EXISTS app_roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);


-- 2. Create application users
CREATE TABLE IF NOT EXISTS app_users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    role_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_user_role
        FOREIGN KEY (role_id)
        REFERENCES app_roles(role_id)
);


-- 3. Define which stores each user can access
CREATE TABLE IF NOT EXISTS user_store_scope (
    user_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, store_id),

    CONSTRAINT fk_scope_user
        FOREIGN KEY (user_id)
        REFERENCES app_users(user_id),

    CONSTRAINT fk_scope_store
        FOREIGN KEY (store_id)
        REFERENCES dim_store(store_id)
);


-- ============================================================
-- INSERT ROLES
-- ============================================================

INSERT INTO app_roles (role_name)
VALUES
    ('Admin'),
    ('Manager'),
    ('Business User')
ON CONFLICT (role_name) DO NOTHING;


-- ============================================================
-- CREATE DEMO USER
-- ============================================================

INSERT INTO app_users (username, role_id)
SELECT
    'van',
    role_id
FROM app_roles
WHERE role_name = 'Manager'
ON CONFLICT (username) DO NOTHING;


-- ============================================================
-- ASSIGN STORE SCOPE
-- User "van" can access Store 1, 2 and 3
-- ============================================================

INSERT INTO user_store_scope (user_id, store_id)
SELECT
    u.user_id,
    s.store_id
FROM app_users u
CROSS JOIN dim_store s
WHERE u.username = 'van'
  AND s.store_id IN (1, 2, 3)
ON CONFLICT DO NOTHING;


-- ============================================================
-- CREATE POSTGRESQL APPLICATION ROLE
-- ============================================================

DO $$
BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM pg_roles
        WHERE rolname = 'retail_app'
    ) THEN

        CREATE ROLE retail_app NOLOGIN;

    END IF;

END
$$;


-- ============================================================
-- GRANT PERMISSIONS TO APPLICATION ROLE
-- ============================================================

GRANT USAGE ON SCHEMA public TO retail_app;

GRANT SELECT ON
    dim_store,
    dim_category,
    dim_product,
    dim_date,
    fact_sales,
    fact_inventory_current,
    app_roles,
    app_users,
    user_store_scope
TO retail_app;


-- Allow postgres to switch to retail_app for testing
GRANT retail_app TO postgres;

-- ============================================================
-- ROW-LEVEL SECURITY
-- ============================================================

-- Enable RLS on sales table
ALTER TABLE fact_sales ENABLE ROW LEVEL SECURITY;


-- Remove old policy if it already exists
DROP POLICY IF EXISTS fact_sales_store_policy
ON fact_sales;


-- Create RLS policy
CREATE POLICY fact_sales_store_policy
ON fact_sales
FOR SELECT
TO retail_app
USING (
    EXISTS (
        SELECT 1
        FROM user_store_scope us
        WHERE us.user_id =
            NULLIF(
                current_setting('app.user_id', true),
                ''
            )::INTEGER

        AND us.store_id = fact_sales.store_id
    )
);
