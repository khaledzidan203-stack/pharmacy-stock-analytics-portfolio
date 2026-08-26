-- Replace :analysis_date with an ISO date such as '2026-08-26'.
WITH sales90 AS (
    SELECT product_id,
           SUM(quantity) AS sales_90d_qty,
           SUM(sales_value_sar) AS sales_90d_value
    FROM sales
    WHERE sales_date BETWEEN date(:analysis_date, '-89 day') AND date(:analysis_date)
    GROUP BY product_id
),
stock AS (
    SELECT product_id,
           SUM(stock_qty) AS stock_qty,
           SUM(CASE WHEN expiry_date < date(:analysis_date) THEN stock_qty ELSE 0 END) AS expired_units,
           SUM(CASE WHEN expiry_date >= date(:analysis_date)
                     AND expiry_date <= date(:analysis_date, '+30 day')
                    THEN stock_qty ELSE 0 END) AS expiring_30d_units
    FROM stock_batches
    GROUP BY product_id
)
SELECT
    COUNT(*) AS sku_count,
    SUM(COALESCE(stock.stock_qty,0)) AS stock_units,
    ROUND(SUM(COALESCE(stock.stock_qty,0) * p.retail_price_sar),2) AS inventory_retail_value_sar,
    SUM(COALESCE(sales90.sales_90d_qty,0)) AS sales_90d_units,
    SUM(COALESCE(stock.expired_units,0) + COALESCE(stock.expiring_30d_units,0)) AS expiry_risk_units
FROM products p
LEFT JOIN sales90 ON sales90.product_id=p.product_id
LEFT JOIN stock ON stock.product_id=p.product_id;
