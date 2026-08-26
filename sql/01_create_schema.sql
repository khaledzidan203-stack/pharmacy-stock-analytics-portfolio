-- SQLite-compatible demo schema
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    item_code TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    retail_price_sar REAL NOT NULL CHECK (retail_price_sar >= 0)
);

CREATE TABLE IF NOT EXISTS sales (
    sales_date TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    sales_value_sar REAL NOT NULL CHECK (sales_value_sar >= 0),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS stock_batches (
    batch_id TEXT PRIMARY KEY,
    product_id INTEGER NOT NULL,
    expiry_date TEXT NOT NULL,
    stock_qty INTEGER NOT NULL CHECK (stock_qty >= 0),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX IF NOT EXISTS ix_sales_product_date ON sales(product_id, sales_date);
CREATE INDEX IF NOT EXISTS ix_stock_product_expiry ON stock_batches(product_id, expiry_date);
