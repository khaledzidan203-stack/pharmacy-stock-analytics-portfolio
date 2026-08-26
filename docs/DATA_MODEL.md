# Data Model

## Grain

- **Products:** one row per SKU.
- **Sales:** one row per SKU per day.
- **Stock batches:** one row per SKU batch / expiry date.
- **Inventory snapshot:** one derived row per SKU at the analysis date.

## Relationships

```text
Products (1) ─────< Sales (many)
    |
    └─────────────< Stock Batches (many)
```

The analytical snapshot is produced by aggregating the two fact-style datasets back to SKU grain before calculating product-level KPIs.

## Why this matters

Joining raw sales rows directly to raw stock-batch rows would create a many-to-many multiplication and overstate quantities. The correct pattern is to aggregate each fact to the desired analytical grain, or model them separately behind a shared product dimension.

## Recommended Power BI model

- `DimProduct`
- `DimDate`
- `FactSales`
- `FactStockBatch`

Use single-direction one-to-many relationships from dimensions to facts. Keep stock expiry calculations in measures or a controlled snapshot table depending on refresh requirements.
