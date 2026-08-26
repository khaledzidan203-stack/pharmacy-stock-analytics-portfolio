-- SKU-level risk analysis.
WITH s AS (
    SELECT product_id, SUM(quantity) AS sales90
    FROM sales
    WHERE sales_date BETWEEN date(:analysis_date, '-89 day') AND date(:analysis_date)
    GROUP BY product_id
),
b AS (
    SELECT product_id,
           SUM(stock_qty) AS stock_qty,
           MIN(expiry_date) AS nearest_expiry,
           SUM(CASE WHEN expiry_date < date(:analysis_date) THEN stock_qty ELSE 0 END) AS expired_units,
           SUM(CASE WHEN expiry_date >= date(:analysis_date) AND expiry_date <= date(:analysis_date,'+30 day') THEN stock_qty ELSE 0 END) AS expiring_30d
    FROM stock_batches
    GROUP BY product_id
),
base AS (
    SELECT p.*,
           COALESCE(s.sales90,0) AS sales90,
           COALESCE(b.stock_qty,0) AS stock_qty,
           COALESCE(b.expired_units,0) AS expired_units,
           COALESCE(b.expiring_30d,0) AS expiring_30d,
           b.nearest_expiry,
           CASE WHEN COALESCE(s.sales90,0)=0 THEN NULL
                ELSE COALESCE(b.stock_qty,0)/(s.sales90/90.0) END AS cover_days
    FROM products p
    LEFT JOIN s ON s.product_id=p.product_id
    LEFT JOIN b ON b.product_id=p.product_id
)
SELECT *,
       CASE WHEN stock_qty>0 AND sales90=0 THEN 1 ELSE 0 END AS dead_stock_flag,
       CASE WHEN stock_qty>0 AND sales90>0 AND cover_days>120 THEN 1 ELSE 0 END AS slow_moving_flag,
       CASE WHEN sales90>0 AND cover_days<14 THEN 1 ELSE 0 END AS reorder_candidate_flag,
       CASE WHEN sales90>0 AND cover_days<14
            THEN MAX(0, CAST(CEIL((sales90/90.0)*30-stock_qty) AS INTEGER)) ELSE 0 END AS reorder_qty_30d
FROM base
ORDER BY reorder_candidate_flag DESC, expired_units + expiring_30d DESC, cover_days ASC;
