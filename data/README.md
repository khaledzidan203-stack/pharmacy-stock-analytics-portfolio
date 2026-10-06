# Synthetic Sample Data

Every CSV in this folder is deterministically generated synthetic data. No row is copied from an operational dataset.

The generator uses fixed seed `20260826` and can recreate the committed sample with:

```bash
python scripts/generate_sample_data.py
```

## Files

- `sample_products.csv` — one row per synthetic SKU.
- `sample_sales_90_days.csv` — one row per SKU per day for the 90-day window.
- `sample_stock_batches.csv` — one row per synthetic stock batch.
- `sample_inventory_snapshot.csv` — one derived analytical row per SKU at the analysis date.

## Current deterministic baseline

- 120 SKUs
- 10,800 daily sales rows
- 231 stock batches
- 90 days: 2026-05-29 through 2026-08-26
