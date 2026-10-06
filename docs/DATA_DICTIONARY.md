# Data Dictionary

## `sample_products.csv`

| Column | Type | Description |
|---|---|---|
| product_id | integer | synthetic surrogate product key |
| item_code | text | synthetic SKU code |
| product_name | text | generic synthetic product name |
| category | text | synthetic analytical category |
| sub_category | text | synthetic analytical subcategory |
| retail_price_sar | decimal | synthetic retail price in SAR |

## `sample_sales_90_days.csv`

| Column | Type | Description |
|---|---|---|
| date | date | synthetic sales date |
| product_id | integer | product foreign key |
| item_code | text | synthetic SKU code for readability |
| quantity | integer | units sold that day |
| sales_value_sar | decimal | quantity × retail price |

## `sample_stock_batches.csv`

| Column | Type | Description |
|---|---|---|
| batch_id | text | synthetic stock-batch key |
| product_id | integer | product foreign key |
| item_code | text | synthetic SKU code |
| expiry_date | date | synthetic expiry date |
| stock_qty | integer | on-hand units in the batch |

## `sample_inventory_snapshot.csv`

| Column | Type | Description |
|---|---|---|
| product_id | integer | product key |
| item_code | text | SKU code |
| product_name | text | product name |
| category | text | category |
| sub_category | text | subcategory |
| retail_price_sar | decimal | retail price |
| stock_qty | integer | total current on-hand stock |
| sales_90d_qty | integer | units sold over 90 days |
| sales_value_90d_sar | decimal | 90-day sales retail value |
| avg_daily_units | decimal | sales_90d_qty / 90 |
| stock_cover_days | decimal/null | stock_qty / unrounded average daily units |
| inventory_value_sar | decimal | stock_qty × retail_price_sar |
| expired_units | integer | units with expiry before analysis date |
| units_expiring_30d | integer | units expiring from analysis date through +30 days |
| nearest_expiry_date | date/null | earliest batch expiry for the SKU |
| dead_stock_flag | 0/1 | stock on hand and zero 90-day sales |
| slow_moving_flag | 0/1 | positive sales and >120 days cover |
| reorder_candidate_flag | 0/1 | positive sales and <14 days cover |
| reorder_qty_30d | integer | simplified 30-day demand less current stock |
