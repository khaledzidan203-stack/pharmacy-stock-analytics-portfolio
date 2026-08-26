# KPI Definitions

All thresholds below are **portfolio assumptions for synthetic demonstration** and should be replaced by business-owned parameters in a production implementation.

| KPI | Formula / rule | Interpretation |
|---|---|---|
| Stock Units | sum of batch stock quantity | on-hand physical units |
| Inventory Retail Value | Stock Units × Retail Price | retail-value proxy, not accounting cost |
| 90-Day Sales Units | sum of sales quantity in last 90 days | recent unit demand |
| Average Daily Units | 90-Day Sales Units / 90 | simple demand velocity |
| Stock Cover Days | Stock Units / Average Daily Units | approximate days of stock at recent velocity |
| Expired Units | expiry date < analysis date | units already past expiry |
| Expiring ≤30d | analysis date ≤ expiry date ≤ analysis date + 30 days | short-dated exposure |
| Dead Stock | stock > 0 and 90-Day Sales = 0 | no movement in analysis window |
| Slow Moving | stock > 0, sales > 0, cover > 120 days | excess cover relative to demand |
| Reorder Candidate | sales > 0 and cover < 14 days | low-cover review queue |
| Reorder Qty 30d | max(0, ceil(30 × Average Daily Units − Stock Units)) | simplified demonstration quantity |

## Important limitations

A production reorder model should consider supplier lead time, safety stock, service-level target, open purchase orders, minimum order quantities, case packs, seasonality, expected promotions, stock in transit, substitution, and cost constraints.
