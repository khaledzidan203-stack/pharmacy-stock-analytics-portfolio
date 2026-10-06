# Pharmacy Inventory & Expiry Analytics

## Demand Velocity, Stock Cover, Expiry Risk & Replenishment Review

[![Quality Checks](https://github.com/khaledzidan203-stack/pharmacy-stock-analytics-portfolio/actions/workflows/quality-checks.yml/badge.svg)](https://github.com/khaledzidan203-stack/pharmacy-stock-analytics-portfolio/actions/workflows/quality-checks.yml)
[![Deploy Dashboard](https://github.com/khaledzidan203-stack/pharmacy-stock-analytics-portfolio/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/khaledzidan203-stack/pharmacy-stock-analytics-portfolio/actions/workflows/deploy-pages.yml)

**Live dashboard:** https://khaledzidan203-stack.github.io/pharmacy-stock-analytics-portfolio/

Pharmacy Inventory & Expiry Analytics is a deterministic synthetic inventory-analysis implementation that combines product master data, 90 days of daily demand and batch-level stock/expiry records to identify low-cover, dead-stock, slow-moving and expiry-risk conditions.

> **Data boundary:** all product names, SKU codes, prices, quantities, sales and expiry dates are synthetic. No real company, customer, patient, employee, prescription, supplier contract, credential, internal system or proprietary operational dataset is included.

<img src="docs/assets/Pharmacy%20Stock%20Analytics%20Dashboard.png" alt="Pharmacy Stock Analytics overview" width="100%">

> **Visual evidence note:** the image above is a presentation schematic. Some illustrative labels, product names, widgets or spreadsheet iconography in the graphic are conceptual only. The authoritative implemented dashboard is the HTML/CSS/JavaScript application in this repository, with retained runtime evidence at `screenshots/dashboard-overview.png`.

**Start here:** [Case study](docs/CASE_STUDY.md) · [Technical walkthrough](docs/TECHNICAL_WALKTHROUGH.md) · [Evidence map](docs/PROJECT_EVIDENCE_MAP.md) · [Project index](docs/PROJECT_INDEX.md) · [Final validation](docs/FINAL_RELEASE_VALIDATION.md)

## Project at a glance

| Area | Current deterministic sample |
|---|---:|
| Analysis date | 26 Aug 2026 |
| Demand window | 90 days |
| SKUs | 120 |
| Daily sales rows | 10,800 |
| Stock batches | 231 |
| Stocked SKUs | 114 |
| Stock Units | 10,682 |
| Inventory Retail Value | SAR 737,970.61 |
| 90-Day Sales Units | 16,337 |
| 90-Day Sales Value | SAR 1,245,983.10 |
| Expired Units | 472 |
| Expiring within 30 days | 1,050 |
| Total Expiry-Risk Units | 1,522 |
| Dead-Stock SKUs | 9 |
| Dead-Stock Retail Value | SAR 8,041.23 |
| Slow-Moving SKUs | 16 |
| Reorder Candidates | 26 |
| Suggested Replenishment Qty | 929 units |

**Stocked SKUs** means SKUs with `stock_qty > 0`. The data model does not contain an Active/Inactive product-status field.

## Business problem

A useful inventory review needs to separate several operational questions:

- Which products have too little stock relative to recent demand?
- Which products carry stock but have no recent sales?
- Which products still sell but hold excessive days of cover?
- Which batches are already expired?
- Which units will expire within the next 30 days?
- Which categories concentrate inventory retail value or risk?
- Which SKU-level actions deserve review first?

The project keeps those risks distinct instead of collapsing them into one stock-status label.

## Analytical flow

```text
Deterministic Synthetic Generator
        ↓
Product Master
Daily Sales × 90 Days
Batch-Level Stock & Expiry
        ↓
Data Quality + Grain Validation
        ↓
Aggregate Sales to SKU
Aggregate Stock / Expiry to SKU
        ↓
Derived SKU Inventory Snapshot
        ↓
Stock Cover · Retail Value · Expiry · Dead · Slow · Reorder
        ↓
Interactive HTML Dashboard
        ↓
Action-Oriented Review
```

The same public model is also translated into SQLite-compatible analytical SQL and a Power BI design blueprint.

## Data model and grain

The project intentionally keeps three source grains separate:

| Dataset | Grain |
|---|---|
| `sample_products.csv` | one row per SKU |
| `sample_sales_90_days.csv` | one SKU per day |
| `sample_stock_batches.csv` | one stock batch per SKU / expiry date |
| `sample_inventory_snapshot.csv` | one derived row per SKU |

This matters because joining raw daily sales directly to raw stock batches would multiply facts and overstate quantities. The correct pattern is to aggregate each fact stream to the desired grain first.

## Governed KPI logic

### Demand

```text
90-Day Sales Units = SUM(Daily Quantity)
Average Daily Units = 90-Day Sales Units / 90
```

### Stock cover

```text
Stock Cover Days = Stock Units / Average Daily Units
```

If 90-day sales are zero, cover remains blank rather than forcing an infinite or misleading number.

### Inventory value

```text
Inventory Retail Value = Stock Units × Retail Price
```

This is a **retail-value analytical proxy**, not accounting inventory cost.

### Expiry exposure

```text
Expired Units:
Expiry Date < Analysis Date

Expiring ≤30d:
Analysis Date ≤ Expiry Date ≤ Analysis Date + 30 days
```

### Dead stock

```text
Stock Units > 0
AND
90-Day Sales Units = 0
```

### Slow moving

```text
Stock Units > 0
AND
90-Day Sales Units > 0
AND
Stock Cover Days > 120
```

### Reorder candidate

```text
90-Day Sales Units > 0
AND
Stock Cover Days < 14
```

### Simplified 30-day reorder quantity

```text
max(
    0,
    ceil(30 × Average Daily Units − Stock Units)
)
```

The reorder formula is a transparent decision-support assumption, not a production replenishment policy.

## Risk flags can overlap

Expiry exposure is independent from Dead / Slow / Reorder classification.

The current synthetic sample includes:

- **7** SKUs that are both Expiry Risk and Reorder Candidates;
- **5** SKUs that are both Dead Stock and Expiry Risk;
- **4** SKUs that are both Slow Moving and Expiry Risk.

This is intentional: a short-dated SKU can still be low-cover, dead or slow-moving.

## Category evidence

For the current synthetic sample:

- **OTC** has the largest inventory retail value: **SAR 298,200.59**.
- OTC has **709** expiry-risk units.
- **Medical Supplies** has **3** dead-stock SKUs.
- Medical Supplies has **302** expiry-risk units.

These are synthetic sample observations only.

## Implemented browser dashboard

The dashboard is built with:

- HTML5
- CSS3
- Vanilla JavaScript
- local CSV inputs
- inline SVG / DOM rendering

Implemented controls:

- Category filter
- Subcategory filter
- Stock View filter
- Reset Filters

Implemented analytical sections:

- KPI summary cards
- Inventory Value by Category
- Inventory Risk Distribution
- 90-Day Sales Trend
- Stock Coverage Distribution
- Priority Reorder Candidates
- Expiry / Dead Stock Attention

### Runtime screenshot

![Implemented dashboard overview](screenshots/dashboard-overview.png)

## Deterministic synthetic generation

`scripts/generate_sample_data.py` uses fixed seed:

`20260826`

It recreates:

- 120 synthetic products;
- 10,800 daily sales rows;
- 231 stock batches;
- the derived 120-row inventory snapshot.

The repository now validates byte-for-byte regeneration with:

```bash
python scripts/check_reproducibility.py
```

## SQLite-compatible analytical layer

The `sql/` directory contains:

- `01_create_schema.sql`
- `02_kpi_queries.sql`
- `03_inventory_risk_queries.sql`
- `04_data_quality_checks.sql`

This layer is **SQLite-compatible**, evidenced by constructs such as `PRAGMA foreign_keys = ON` and SQLite date functions.

The SQL provides a relational translation of the same product, sales, stock-batch and risk logic. It is not the runtime engine behind the browser dashboard.

## Power BI boundary

`docs/POWER_BI_GUIDE.md` provides a design blueprint for:

- `DimProduct`
- `DimDate`
- `FactSales`
- `FactStockBatch`
- suggested DAX measures
- suggested inventory-health report pages

There is currently **no committed PBIP, PBIR, TMDL, PBIX or PBIT runtime implementation**.

Power BI is therefore design guidance only.

## Automated validation

GitHub Actions validates:

- exact source-data row counts;
- 90-day date window;
- key uniqueness;
- product-reference integrity;
- non-negative sales and stock quantities;
- Sales Value reconciliation;
- Average Daily Units;
- Stock Cover;
- Inventory Retail Value;
- expired-unit logic;
- 30-day expiry logic;
- nearest expiry;
- Dead Stock flag;
- Slow Moving flag;
- Reorder Candidate flag;
- simplified reorder quantity;
- aggregate KPI baselines;
- risk overlap baselines;
- category evidence baselines;
- deterministic regeneration of all four CSV files;
- common secret / PII-like patterns;
- JavaScript syntax.

## Quick start

### Run the dashboard

```bash
python -m http.server 8000
```

Open:

`http://localhost:8000`

### Regenerate and validate

```bash
python scripts/generate_sample_data.py
python scripts/check_reproducibility.py
python scripts/validate_repository.py
python -m pytest -q
```

The generator itself uses only the Python standard library. `pytest` is the optional automated-test dependency.

## Repository structure

```text
data/                  synthetic products, daily sales, stock batches, SKU snapshot
scripts/               generator, validator, reproducibility check
tests/                 source-data and analytical regression tests
index.html             browser dashboard shell
src/css/               dashboard styling
src/js/                analytical rendering and filters
sql/                   SQLite-compatible model and queries
screenshots/           retained dashboard runtime evidence
examples/              synthetic KPI and narrative examples
docs/                  analytical, business, governance and evidence documentation
docs/assets/           presentation assets
.github/workflows/     quality gate + GitHub Pages deployment
```

## Documentation

- [Project Index](docs/PROJECT_INDEX.md)
- [Case Study](docs/CASE_STUDY.md)
- [Technical Walkthrough](docs/TECHNICAL_WALKTHROUGH.md)
- [Project Evidence Map](docs/PROJECT_EVIDENCE_MAP.md)
- [Business Requirements](docs/BUSINESS_REQUIREMENTS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Data Model](docs/DATA_MODEL.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [KPI Definitions](docs/KPI_DEFINITIONS.md)
- [Analytical Methodology](docs/ANALYTICAL_METHODOLOGY.md)
- [Assumptions](docs/ASSUMPTIONS.md)
- [Power BI Blueprint](docs/POWER_BI_GUIDE.md)
- [Repository Verification](docs/REPOSITORY_VERIFICATION.md)
- [Final Release Validation](docs/FINAL_RELEASE_VALIDATION.md)

## Limitations

- All data is synthetic.
- Analysis uses a fixed 90-day demand window.
- Inventory value uses retail price rather than cost.
- Reorder logic omits supplier lead time, safety stock, service-level targets, open POs, MOQ, case packs, promotions and stock in transit.
- No branch/location dimension is modeled.
- No forecasting or causal inference is claimed.
- SQLite source is not the browser dashboard runtime.
- Power BI is design-only.
- The presentation infographic is schematic and may contain illustrative labels not present in the implementation.

Licensed under the [MIT License](LICENSE).
