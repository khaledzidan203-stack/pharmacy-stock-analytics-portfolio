# Power BI Implementation Blueprint

> **Implementation status — design guidance only.** The repository does not contain a PBIP, PBIR, TMDL, PBIX or PBIT runtime artifact.

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

1. Executive Inventory Health
2. Replenishment Review
3. Expiry & Slow Moving
4. Category Exposure
5. Data Quality

## Recommended UX

- Slicers for Category, Subcategory and date.
- Clear distinction between Expiry, Dead Stock, Slow Moving and Reorder.
- Drill-through from Category to SKU.
- Methodology page showing the 14 / 30 / 120-day assumptions.
- Explicit retail-value proxy label.

## Evidence boundary

These DAX and modeling notes have not been executed in a committed Power BI runtime file. The implemented reporting artifact is the HTML/CSS/JavaScript dashboard.
