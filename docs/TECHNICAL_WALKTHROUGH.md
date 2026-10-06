# Technical Walkthrough — 60–90 Seconds

**0–10 seconds — Scope**

This project is a deterministic synthetic pharmacy inventory analytics implementation covering demand, batch stock, expiry exposure, stock cover and replenishment review.

**10–25 seconds — Grain**

Products are stored at SKU grain, sales at SKU × day grain, and inventory at batch × expiry-date grain. The current sample has 120 SKUs, 10,800 daily sales rows and 231 stock batches.

**25–40 seconds — Analytical preparation**

Sales are aggregated to trailing-90-day demand. Stock batches are aggregated to on-hand stock while retaining expired and next-30-day exposure. The two fact streams are joined only after aggregation to SKU grain.

**40–55 seconds — KPI logic**

The snapshot calculates Average Daily Units, Stock Cover Days, Inventory Retail Value, Dead Stock, Slow Moving, Reorder Candidate and a simplified 30-day replenishment quantity.

**55–70 seconds — Interactive output**

The HTML/CSS/Vanilla JavaScript dashboard provides Category, Subcategory and Stock View filters plus KPI cards, category value, risk distribution, sales trend, coverage distribution and action tables.

**70–80 seconds — Validation**

Python tests verify deterministic regeneration, row counts, key integrity, snapshot formulas, current KPI baselines and risk classifications.

**80–90 seconds — Tool boundary**

The SQL layer is SQLite-compatible. Power BI content is a blueprint only; no PBIX/PBIP/PBIR/TMDL runtime implementation is claimed.
