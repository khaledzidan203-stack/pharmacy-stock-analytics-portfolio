-- 1. Duplicate product codes
SELECT item_code, COUNT(*) AS row_count
FROM products
GROUP BY item_code
HAVING COUNT(*) > 1;

-- 2. Orphan sales rows
SELECT s.*
FROM sales s
LEFT JOIN products p ON p.product_id=s.product_id
WHERE p.product_id IS NULL;

-- 3. Orphan stock rows
SELECT b.*
FROM stock_batches b
LEFT JOIN products p ON p.product_id=b.product_id
WHERE p.product_id IS NULL;

-- 4. Invalid quantities or prices (should return no rows with schema checks enabled)
SELECT * FROM products WHERE retail_price_sar < 0;
SELECT * FROM sales WHERE quantity < 0 OR sales_value_sar < 0;
SELECT * FROM stock_batches WHERE stock_qty < 0;

-- 5. Suspicious missing / blank values
SELECT * FROM products
WHERE TRIM(item_code)='' OR TRIM(product_name)='' OR TRIM(category)='';
