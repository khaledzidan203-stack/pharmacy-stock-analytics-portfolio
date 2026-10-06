# Case Study — Pharmacy Inventory & Expiry Intelligence

## Context

Inventory teams need to distinguish several operational problems that can look similar in a simple stock report:

- low stock relative to recent demand;
- excess stock with positive but slow movement;
- on-hand stock with no recent sales;
- already expired units;
- short-dated stock approaching expiry.

This project models those problems separately using deterministic synthetic pharmacy inventory data.

## Data design

The analytical model combines three normalized source grains:

- **Product** — one row per SKU;
- **Sales** — one row per SKU per day;
- **Stock Batch** — one row per SKU batch / expiry date.

The dashboard consumes a derived SKU-level snapshot created only after sales and stock-batch facts are aggregated to product grain.

This avoids many-to-many multiplication between daily sales rows and stock batches.

## Deterministic synthetic baseline

The generated sample uses fixed seed `20260826` and analysis date `2026-08-26`.

Current committed data:

- 120 SKUs;
- 10,800 daily sales rows;
- 231 stock batches;
- 90 days from 2026-05-29 through 2026-08-26;
- 10,682 stock units;
- SAR 737,970.61 inventory retail-value proxy;
- 16,337 units sold;
- SAR 1,245,983.10 90-day sales value.

## Risk segmentation

The synthetic snapshot currently contains:

- 472 already expired units;
- 1,050 units expiring within 30 days;
- 1,522 total expiry-risk units;
- 9 dead-stock SKUs;
- SAR 8,041.23 dead-stock retail value;
- 16 slow-moving SKUs;
- 26 reorder candidates;
- 929 simplified suggested replenishment units.

Risk flags are **not mutually exclusive**.

For example, the current sample includes:

- 7 SKUs that are both expiry-risk and reorder candidates;
- 5 SKUs that are both dead stock and expiry-risk;
- 4 SKUs that are both slow-moving and expiry-risk.

This is analytically useful because stock health should not be collapsed into one exclusive status.

## Category evidence

The current synthetic sample shows:

- OTC inventory retail value: SAR 298,200.59;
- OTC expiry-risk units: 709;
- Medical Supplies dead-stock SKUs: 3;
- Medical Supplies expiry-risk units: 302.

These are synthetic sample findings, not real-company observations.

## Reorder logic

The public demonstration uses:

`Reorder Candidate = positive 90-day sales AND Stock Cover < 14 days`

and:

`Reorder Qty 30d = max(0, ceil(30 × Average Daily Units − Stock Units))`

This is a simplified decision-support rule. It is not a production replenishment policy because supplier lead time, safety stock, service level, open purchase orders, MOQ, case pack, promotion and cost constraints are outside the public model.

## Delivery architecture

The project includes:

- deterministic Python data generation;
- Python repository/data validation;
- automated pytest regression checks;
- HTML/CSS/Vanilla JavaScript dashboard;
- SQLite-compatible schema and analytical queries;
- GitHub Pages deployment workflow;
- Power BI design guidance.

## Outcome

The implemented analytical sequence is:

**90-Day Demand → Batch Stock & Expiry → SKU Snapshot → Stock Cover → Expiry / Dead / Slow / Reorder Flags → Action-Oriented Review**
