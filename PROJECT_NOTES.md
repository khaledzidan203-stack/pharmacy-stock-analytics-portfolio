# Project Notes

## Purpose

Pharmacy Inventory & Expiry Analytics demonstrates a deterministic, synthetic inventory-analysis workflow for stock health, demand velocity, expiry exposure and replenishment review.

## Core design choices

1. **Deterministic synthetic data** — the generator uses fixed seed `20260826`.
2. **Explicit grain separation** — products, daily sales and stock batches remain separate until analytical aggregation.
3. **SKU-level decision layer** — the derived snapshot is the primary operational review grain.
4. **Retail-value transparency** — inventory value uses synthetic retail price as a proxy and is not presented as accounting cost.
5. **Distinct risk concepts** — expiry, dead stock, slow movement and reorder need are separate flags and may overlap.
6. **Simplified replenishment logic** — the 30-day suggested quantity is a transparent analytical assumption, not an execution policy.
7. **Dependency-light delivery** — the dashboard uses HTML/CSS/Vanilla JavaScript and the generator uses the Python standard library.
8. **Tool boundaries** — SQLite-compatible SQL is implemented; Power BI remains a blueprint only.

## Implemented layers

- deterministic synthetic-data generation;
- product / daily sales / stock-batch source files;
- derived SKU-level analytical snapshot;
- interactive web dashboard;
- automated validation and regression tests;
- SQLite-compatible analytical SQL;
- GitHub Pages workflow;
- Power BI implementation guide.

## Scaling path

A production implementation would typically add branch/location inventory, supplier lead times, open purchase orders, service-level targets, safety stock, MOQ/case packs, cost valuation, demand forecasting and governed business-owned threshold tables.
