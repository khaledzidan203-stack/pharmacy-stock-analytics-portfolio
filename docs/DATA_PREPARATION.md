# Data Preparation

## Required inputs

1. Product master with unique SKU, category, subcategory and price.
2. Recent sales with date, SKU and quantity.
3. Stock-batch data with SKU, expiry date and stock quantity.

## Preparation steps

1. Standardize SKU identifiers.
2. Enforce a unique product key in the product master.
3. Parse dates using ISO format `YYYY-MM-DD`.
4. Reject negative stock and sales quantities.
5. Verify all sales and stock product references exist.
6. Aggregate daily sales to 90-day SKU totals.
7. Calculate average daily units.
8. Aggregate stock batches to current SKU stock.
9. Calculate expired and next-30-day exposure relative to the analysis date.
10. Preserve nearest batch expiry.
11. Join sales and stock aggregates at SKU grain.
12. Calculate cover, retail-value proxy and risk flags.
13. Calculate the simplified 30-day reorder quantity.
14. Run repository and regression validation.

## Reproducibility

The generator uses fixed random seed `20260826`.

Run:

```bash
python scripts/check_reproducibility.py
```

The check regenerates all four public CSVs and verifies that they match the committed versions byte-for-byte.
