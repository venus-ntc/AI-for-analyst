CREATE INDEX IF NOT EXISTS idx_sales_date
ON fact_sales(sale_date);

CREATE INDEX IF NOT EXISTS idx_sales_store
ON fact_sales(store_id);

CREATE INDEX IF NOT EXISTS idx_sales_product
ON fact_sales(product_id);

CREATE INDEX IF NOT EXISTS idx_sales_store_date
ON fact_sales(store_id, sale_date);

CREATE INDEX IF NOT EXISTS idx_inventory_store
ON fact_inventory_current(store_id);

CREATE INDEX IF NOT EXISTS idx_inventory_product
ON fact_inventory_current(product_id);
