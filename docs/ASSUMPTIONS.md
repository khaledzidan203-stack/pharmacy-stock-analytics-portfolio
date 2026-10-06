# Assumptions

- Analysis date: 2026-08-26.
- Demand window: trailing 90 days.
- Reorder-review threshold: stock cover below 14 days.
- Expiry-risk horizon: 30 days.
- Slow-moving threshold: stock cover above 120 days with positive sales.
- Zero-sales stock is classified separately as Dead Stock.
- Inventory value uses synthetic retail price as a **retail-value analytical proxy**, not governed accounting cost.
- Reorder quantity uses a simplified 30-day demand-minus-stock calculation.
- Supplier lead time, safety stock, open purchase orders, MOQ, case packs, promotions, substitution, transfers and service-level targets are not modeled.
- Risk flags are not mutually exclusive.
- All thresholds are synthetic demonstration parameters and should be business-owned in a production implementation.
