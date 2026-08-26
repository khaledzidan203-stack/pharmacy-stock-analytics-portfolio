# Data Preparation

## Required inputs

1. Product master with unique SKU, category, subcategory, and price.
2. Recent sales with date, SKU, and quantity.
3. Stock-batch data with SKU, expiry date, and stock quantity.

## Preparation steps

1. Trim and standardize SKU identifiers.
2. Enforce a unique product key in the product master.
3. Parse dates using an unambiguous ISO format (`YYYY-MM-DD`) in the public sample.
4. Reject or flag negative stock quantity and impossible sales quantities unless returns are explicitly modeled.
5. Verify all sales and stock SKUs exist in the product master.
6. Aggregate sales to 90-day SKU totals and calculate average daily demand.
7. Aggregate batch stock to current SKU stock.
8. Calculate expiry exposure from batch dates relative to the analysis date.
9. Join the aggregates at SKU grain.
10. Calculate coverage, inventory value, dead/slow/reorder flags, and demonstration reorder quantity.

## Reproducibility

Run:

```bash
python scripts/generate_sample_data.py
python scripts/validate_repository.py
```

The generated data is deterministic and does not require access to any private source file.
