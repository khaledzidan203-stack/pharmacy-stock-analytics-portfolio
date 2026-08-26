# Example Analysis Output

This example is generated from the repository's synthetic data and illustrates the type of business narrative the model supports.

## Sample KPI snapshot

- Stock units: **10,682**
- Inventory retail value: **SAR 737,971**
- 90-day sales: **16,337 units**
- Expired / next-30-day units: **1,522**
- Dead stock retail value: **SAR 8,041**
- Reorder candidate SKUs: **26**

## Example interpretation

The workflow does not treat all low-performing inventory the same way. Products with zero recent demand are separated from slow movers that still sell, while expiry exposure is assessed from batch dates. Low-cover products are surfaced separately as replenishment candidates. This allows an analyst to create distinct operational queues instead of relying on a single stock-status label.

These figures come only from the synthetic sample contained in this repository.
