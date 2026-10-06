# Presentation Assets

This directory contains presentation-only visual assets for the Pharmacy Inventory & Expiry Analytics project.

## Intended use

The primary overview image stored here is used by the repository README to summarize the analytical workflow at a glance.

Recommended filename:

`pharmacy_inventory_expiry_analytics_overview.png`

The overview should represent only repository-supported claims, including:

- deterministic synthetic data generated with seed `20260826`;
- 120 synthetic SKUs;
- 10,800 daily sales rows covering a 90-day window;
- 231 synthetic stock batches;
- SKU-level analytical snapshot;
- Stock Units and Inventory Retail Value;
- 90-Day Sales Units and Sales Value;
- Stock Cover Days;
- Expired Units and Units Expiring Within 30 Days;
- Dead Stock, Slow Moving, and Reorder Candidate flags;
- simplified 30-day replenishment quantity;
- Category and Subcategory filtering;
- action-oriented reorder and expiry/dead-stock tables;
- HTML/CSS/Vanilla JavaScript dashboard;
- Python synthetic-data generation and validation;
- SQLite-compatible schema, KPI queries, inventory-risk queries, and data-quality checks;
- Power BI implementation guide/design blueprint only;
- GitHub Actions quality checks and GitHub Pages deployment.

## Evidence boundary

Assets in this directory are presentation summaries only. They are not source data, runtime validation evidence, SQLite execution evidence, Power BI runtime evidence, or proof of any real pharmacy operation.

Authoritative claims remain defined by the committed synthetic CSV files, generator, validator, HTML/JavaScript implementation, SQL scripts, automated tests, documentation, screenshots, and GitHub Actions workflows.

Inventory Retail Value is a retail-price proxy, not an accounting cost valuation. Reorder logic is a simplified analytical assumption and not a production replenishment policy.
