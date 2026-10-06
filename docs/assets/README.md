# Presentation Assets

This directory contains presentation-only visual assets for the Pharmacy Inventory & Expiry Analytics project.

## Current overview

`Pharmacy Stock Analytics Dashboard.png`

The repository README uses this image as a high-level presentation schematic.

## Evidence-supported scope

The implemented repository supports:

- 120 deterministic synthetic SKUs;
- 10,800 daily sales rows across a 90-day window;
- 231 synthetic stock batches;
- 10,682 stock units;
- SAR 737,970.61 inventory retail-value proxy;
- 16,337 90-day sales units;
- SAR 1,245,983.10 90-day sales value;
- 472 expired units;
- 1,050 units expiring within 30 days;
- 9 dead-stock SKUs;
- 16 slow-moving SKUs;
- 26 reorder candidates;
- 929 simplified suggested replenishment units;
- HTML/CSS/Vanilla JavaScript dashboard;
- deterministic Python data generation and validation;
- SQLite-compatible analytical SQL;
- GitHub Pages deployment;
- Power BI design guidance.

## Evidence boundary

The infographic is a **presentation schematic**, not a literal screenshot of the implemented dashboard.

The authoritative implemented dashboard is `index.html` + `src/`, with retained runtime evidence at `screenshots/dashboard-overview.png`.

Any illustrative category labels, product names, visual widgets, spreadsheet iconography or layout concepts shown in the infographic that are not present in the committed repository should be treated as conceptual only.

The repository does **not** contain an Excel analytical workbook and does **not** contain a Power BI runtime file.

Inventory Retail Value is based on synthetic retail price and is not an accounting-cost valuation. Reorder quantities are simplified decision-support outputs, not production purchase orders.
