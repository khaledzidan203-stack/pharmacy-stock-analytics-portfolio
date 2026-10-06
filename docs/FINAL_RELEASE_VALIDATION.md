# Final Release Validation

## Release scope

This hardening release strengthens terminology, reproducibility, KPI regression coverage, implementation boundaries and public presentation without changing the deterministic generator logic, committed synthetic dataset, HTML analytical engine, CSS design, SQLite SQL logic or retained runtime screenshot.

## Automated analytical contract

The quality gate validates:

- 120 unique products;
- 10,800 daily sales rows;
- exactly 90 dates;
- 231 stock batches;
- no orphan product references;
- no negative sales or stock quantities;
- one derived snapshot row per product;
- row-level Sales Value formula;
- Average Daily Units formula;
- Stock Cover formula;
- Inventory Retail Value formula;
- expired and next-30-day unit logic;
- nearest expiry;
- Dead Stock flag;
- Slow Moving flag;
- Reorder Candidate flag;
- simplified 30-day reorder quantity;
- current aggregate KPI baseline;
- deterministic regeneration of all four committed CSV files;
- common secret / PII-like text patterns;
- JavaScript syntax.

## Current aggregate baseline

- Stocked SKUs: 114
- Stock Units: 10,682
- Inventory Retail Value: SAR 737,970.61
- 90-Day Sales Units: 16,337
- 90-Day Sales Value: SAR 1,245,983.10
- Expired Units: 472
- Expiring ≤30d Units: 1,050
- Dead Stock: 9 SKUs / SAR 8,041.23
- Slow Moving: 16 SKUs
- Reorder Candidates: 26 SKUs
- Suggested Replenishment: 929 units

## Runtime boundaries

- Browser dashboard: implemented.
- GitHub Pages: deployment workflow retained.
- Python generator/validator/tests: implemented.
- SQLite-compatible SQL: implemented source.
- Power BI: design blueprint only.
- Inventory value: retail-price proxy, not accounting-cost valuation.

## Presentation boundary

The uploaded infographic is presentation-only. The retained dashboard screenshot and executable web application are the runtime evidence.
