# Repository Verification

## Current validation contract

The repository is validated through GitHub Actions and can also be checked locally with:

```bash
python scripts/validate_repository.py
python scripts/check_reproducibility.py
python -m pytest -q
node --check src/js/app.js
```

## Analytical checks

The current release verifies:

- 120 synthetic products;
- 10,800 daily sales rows;
- 231 stock batches;
- exactly 90 sales dates;
- one SKU-level snapshot row per product;
- unique product and item-code keys;
- no orphan sales or stock references;
- no negative sales or stock quantities;
- Sales Value formula;
- Average Daily Units;
- Stock Cover;
- Inventory Retail Value;
- expired-unit logic;
- next-30-day expiry logic;
- nearest expiry;
- Dead Stock flag;
- Slow Moving flag;
- Reorder Candidate flag;
- simplified 30-day reorder quantity;
- aggregate KPI baselines;
- risk-overlap baselines;
- deterministic byte-for-byte regeneration.

## Current baseline

- Stocked SKUs: 114
- Stock Units: 10,682
- Inventory Retail Value: SAR 737,970.61
- 90-Day Sales Units: 16,337
- 90-Day Sales Value: SAR 1,245,983.10
- Expired Units: 472
- Expiring ≤30d: 1,050
- Dead Stock: 9 SKUs
- Slow Moving: 16 SKUs
- Reorder Candidates: 26 SKUs
- Suggested Replenishment: 929 units

## Confidentiality checks

- No production spreadsheet or source export is required.
- Product names, SKU codes, prices, quantities, sales and expiry dates are synthetic.
- Common secret, credential, network and PII-like patterns are scanned in public text files.
- Analytical thresholds are explicitly synthetic assumptions.

## Tool boundaries

- Browser dashboard: implemented.
- SQLite-compatible SQL: committed source.
- GitHub Pages workflow: implemented.
- Power BI: design guidance only.
- Excel analytical workbook: not part of this repository.

## Interpretation

A passing validation establishes consistency with the committed synthetic analytical contract. It does not establish production readiness or approval of real-world replenishment policy.
