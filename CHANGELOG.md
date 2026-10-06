# Changelog

## Unreleased — Inventory Analytics Hardening

- Rebuilt the project presentation around inventory, demand, expiry and replenishment intelligence.
- Corrected the 114-SKU label from **Active SKUs** to **Stocked SKUs** because the data model has no Active/Inactive status field.
- Added deterministic byte-for-byte regeneration validation.
- Added analytical regression tests for KPI baselines and row-level snapshot formulas.
- Added explicit risk-overlap tests for Expiry + Reorder, Expiry + Dead Stock and Expiry + Slow Moving.
- Clarified that Inventory Retail Value is a retail-price proxy rather than accounting cost.
- Clarified the simplified 30-day reorder quantity as decision support rather than purchase-order logic.
- Clarified that SQL scripts are SQLite-compatible.
- Clarified that Power BI is a design blueprint only.
- Replaced recruitment-oriented notes with neutral project notes.
- Added project index, case study, walkthrough, evidence map, environment baseline and final validation documentation.
- Added a presentation infographic while retaining the real dashboard screenshot as runtime evidence.
- Expanded CI quality gates and GitHub Pages deployment behavior.

## 1.0.0 — 2026-08-26

### Added

- Synthetic product, 90-day sales, stock-batch and analytical snapshot datasets.
- Interactive HTML inventory and expiry dashboard.
- SQLite-compatible schema, KPI queries, risk queries and data-quality checks.
- Business requirements, architecture, data model, data dictionary, KPI definitions, methodology, setup, usage, Power BI guidance and privacy documentation.
- Example KPI outputs.
- Repository validation tests and GitHub Actions workflows.

### Privacy

- Public data is synthetic and analytical rules are generalized.
