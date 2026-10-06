# Analytical Methodology

## 1. Define the decision grain

The primary decision grain is SKU. Batch data is aggregated to SKU for stock coverage while batch expiry information remains available for expiry-risk calculations.

## 2. Establish recent demand

Use the trailing 90-day sales window as a simple, explainable proxy for recent demand. Daily rows are retained so demand trends can also be visualized.

## 3. Separate inventory problems

The model keeps distinct operational questions separate:

- **Low cover:** demand exists but on-hand stock is low relative to recent velocity.
- **Dead stock:** stock exists but no sales occurred in the 90-day window.
- **Slow moving:** sales exist, but cover is high relative to recent demand.
- **Expiry risk:** stock is already expired or will expire within the configured horizon.

A SKU can carry more than one flag. Expiry exposure is intentionally independent from Dead / Slow / Reorder classification.

## 4. Aggregate facts before joining

Daily sales and stock batches are different fact grains. They are each aggregated to SKU before being combined in the analytical snapshot.

This avoids many-to-many row multiplication.

## 5. Aggregate for management views

SKU outputs can be summarized by Category or Subcategory while action tables retain SKU-level detail.

## 6. Validate before interpretation

Validation checks include:

- duplicate product keys;
- orphan references;
- negative quantities;
- 90-day date-window integrity;
- Sales Value reconciliation;
- Stock / Expiry reconciliation;
- snapshot formulas;
- Dead / Slow / Reorder flags;
- aggregate KPI baselines;
- deterministic regeneration.

## 7. Treat thresholds as governed parameters

The public implementation uses:

- Reorder review: <14 days cover
- Expiry horizon: 30 days
- Slow moving: >120 days cover

These are synthetic demonstration assumptions. A production system should store business-owned thresholds in a governed parameter layer.
