# Analytical Methodology

## 1. Define the decision grain

The primary decision grain is SKU. Batch data is aggregated to SKU for stock coverage while retaining batch expiry information for expiry risk.

## 2. Establish recent demand

Use the trailing 90-day sales window as a simple, explainable proxy for recent demand. The synthetic demo retains daily rows so trends can also be visualized.

## 3. Separate inventory problems

The model keeps different problems distinct:

- **Low cover:** demand exists but on-hand stock is low.
- **Dead stock:** stock exists but no sales occurred in the 90-day window.
- **Slow moving:** sales exist, but stock is disproportionately high relative to recent demand.
- **Expiry risk:** stock has already expired or is approaching expiry.

A SKU can have more than one flag, which is often operationally important.

## 4. Aggregate for management views

SKU outputs are aggregated by category/subcategory for portfolio-level comparisons, while action tables preserve SKU detail.

## 5. Validate before interpretation

Checks include duplicate keys, negative quantities, missing product references, invalid dates, price issues, and reconciliation between batch stock and snapshot stock.

## 6. Treat thresholds as parameters

The public thresholds are assumptions. In production they should be stored in a governed parameter table and approved by business owners.
