# Power BI Implementation Guide

## Recommended tables

- `DimProduct` ← `sample_products.csv`
- `DimDate` ← generated calendar table
- `FactSales` ← `sample_sales_90_days.csv`
- `FactStockBatch` ← `sample_stock_batches.csv`

## Relationships

- `DimProduct[product_id]` 1 → * `FactSales[product_id]`
- `DimProduct[product_id]` 1 → * `FactStockBatch[product_id]`
- `DimDate[Date]` 1 → * `FactSales[date]`

Use single-direction filtering from dimensions to facts.

## Example DAX measures

```DAX
Sales Units =
SUM ( FactSales[quantity] )

Sales Value =
SUM ( FactSales[sales_value_sar] )

Stock Units =
SUM ( FactStockBatch[stock_qty] )

Inventory Retail Value =
SUMX (
    DimProduct,
    CALCULATE ( [Stock Units] ) * DimProduct[retail_price_sar]
)

Sales Units 90D =
CALCULATE (
    [Sales Units],
    DATESINPERIOD ( DimDate[Date], MAX ( DimDate[Date] ), -90, DAY )
)

Average Daily Units 90D =
DIVIDE ( [Sales Units 90D], 90 )

Stock Cover Days =
DIVIDE ( [Stock Units], [Average Daily Units 90D] )

Expired Units =
VAR AnalysisDate = MAX ( DimDate[Date] )
RETURN
CALCULATE (
    [Stock Units],
    FactStockBatch[expiry_date] < AnalysisDate
)

Expiring 30D Units =
VAR AnalysisDate = MAX ( DimDate[Date] )
RETURN
CALCULATE (
    [Stock Units],
    FactStockBatch[expiry_date] >= AnalysisDate,
    FactStockBatch[expiry_date] <= AnalysisDate + 30
)
```

## Suggested report pages

### 1. Executive Inventory Health
- KPI cards
- Category inventory value
- Risk classification
- sales trend

### 2. Replenishment Review
- low-cover SKU table
- stock cover distribution
- recent sales trend

### 3. Expiry & Slow Moving
- expired / short-dated units
- dead stock value
- slow-moving table
- category exposure

### 4. Data Quality
- orphan product references
- duplicate keys
- negative or missing values
- reconciliation checks

## Recommended UX

- Use slicers for category, subcategory, and date.
- Keep status colors semantic and consistent.
- Add drill-through from category views to SKU details.
- Put threshold assumptions in an information tooltip or dedicated methodology page.
