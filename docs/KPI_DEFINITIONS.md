# KPI Definitions

All thresholds below are synthetic demonstration assumptions and should become governed business parameters in a production implementation.

| KPI | Formula / rule | Interpretation |
|---|---|---|
| Total SKUs | COUNT(product_id) | synthetic assortment size |
| Stocked SKUs | COUNT where Stock Units > 0 | SKUs with on-hand stock; not an Active/Inactive status |
| Stock Units | SUM(batch stock quantity) | on-hand physical units |
| Inventory Retail Value | SUM(Stock Units × Retail Price) | retail-value proxy, not accounting cost |
| 90-Day Sales Units | SUM(sales quantity) | recent unit demand |
| 90-Day Sales Value | SUM(quantity × retail price) | synthetic sales retail value |
| Average Daily Units | 90-Day Sales Units / 90 | simple demand velocity |
| Stock Cover Days | Stock Units / Average Daily Units | approximate days of stock at recent velocity |
| Expired Units | expiry date < analysis date | units already past expiry |
| Expiring ≤30d | analysis date ≤ expiry date ≤ analysis date + 30 days | short-dated exposure |
| Dead Stock | stock > 0 and 90-Day Sales = 0 | stocked SKU with no movement in analysis window |
| Slow Moving | stock > 0, sales > 0, cover > 120 days | high cover relative to recent demand |
| Reorder Candidate | sales > 0 and cover < 14 days | low-cover review queue |
| Reorder Qty 30d | max(0, ceil(30 × Average Daily Units − Stock Units)) | simplified decision-support quantity |

## Risk interaction

Dead Stock, Slow Moving, Reorder and Expiry are separate analytical concepts. Expiry exposure can overlap with another risk flag.

## Current synthetic baseline

- Total SKUs: 120
- Stocked SKUs: 114
- Stock Units: 10,682
- Inventory Retail Value: SAR 737,970.61
- 90-Day Sales Units: 16,337
- 90-Day Sales Value: SAR 1,245,983.10
- Expired Units: 472
- Expiring ≤30d: 1,050
- Dead Stock: 9 SKUs
- Slow Moving: 16 SKUs
- Reorder Candidates: 26 SKUs
- Simplified Reorder Quantity: 929 units

## Production limitations

A production replenishment model should consider supplier lead time, safety stock, service-level target, open purchase orders, MOQ, case packs, seasonality, promotions, stock in transit, substitution, transfer opportunities and cost constraints.
