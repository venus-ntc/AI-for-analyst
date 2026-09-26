SELECT COUNT(*) AS total_sales
FROM fact_sales;


SELECT COUNT(*) AS total_products
FROM dim_product;

SELECT COUNT(*) AS total_stores
FROM dim_store;

SELECT
    SUM(
        s.units * p.product_price
    ) AS total_revenue

FROM fact_sales s

JOIN dim_product p
    ON s.product_id = p.product_id;


SELECT
    SUM(
        s.units *
        (
            p.product_price
            - p.product_cost
        )
    ) AS gross_profit

FROM fact_sales s

JOIN dim_product p
    ON s.product_id = p.product_id;


SELECT
    c.category_name,

    SUM(
        s.units * p.product_price
    ) AS revenue

FROM fact_sales s

JOIN dim_product p
    ON s.product_id = p.product_id

JOIN dim_category c
    ON p.category_id = c.category_id

GROUP BY c.category_name

ORDER BY revenue DESC;


SELECT
    st.store_name,

    SUM(
        s.units * p.product_price
    ) AS revenue

FROM fact_sales s

JOIN dim_store st
    ON s.store_id = st.store_id

JOIN dim_product p
    ON s.product_id = p.product_id

GROUP BY
    st.store_id,
    st.store_name

ORDER BY revenue DESC;


SELECT
    d.year,
    d.month,
    d.month_name,

    SUM(
        s.units * p.product_price
    ) AS revenue

FROM fact_sales s

JOIN dim_product p
    ON s.product_id = p.product_id

JOIN dim_date d
    ON s.sale_date = d.date

GROUP BY
    d.year,
    d.month,
    d.month_name

ORDER BY
    d.year,
    d.month;


SELECT
    st.store_name,
    p.product_name,
    i.stock_on_hand

FROM fact_inventory_current i

JOIN dim_store st
    ON i.store_id = st.store_id

JOIN dim_product p
    ON i.product_id = p.product_id

WHERE i.stock_on_hand = 0;
