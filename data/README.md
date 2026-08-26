# Synthetic Sample Data

Every CSV in this folder is generated data for portfolio demonstration. No row is copied from an operational dataset.

The generator is deterministic so reviewers can reproduce the sample using `python scripts/generate_sample_data.py`.

## Files

- `sample_products.csv` — product master
- `sample_sales_90_days.csv` — daily unit sales for a 90-day window
- `sample_stock_batches.csv` — stock quantity at batch/expiry grain
- `sample_inventory_snapshot.csv` — derived SKU-level analytics output
