# Portfolio Notes — Pharmacy Inventory & Expiry Analytics

## What I personally built

I designed the project as an end-to-end analytics solution: I framed the inventory problem, defined the analytical entities, created the KPI logic, structured the data-preparation flow, designed the dashboard experience, implemented the HTML/CSS/JavaScript dashboard, wrote SQL versions of the analysis, documented a Power BI implementation path, and created a synthetic-data strategy so the work can be discussed publicly without exposing operational data.

## Analytical skills demonstrated

- Translating operational questions into measurable KPIs
- Joining data at different grains: product master, daily sales, and stock batches
- Separating raw facts from derived analytical outputs
- Sales-velocity and stock-cover calculations
- Expiry-risk segmentation
- Dead-stock and slow-moving identification
- Reorder prioritization using recent demand
- Category-level aggregation and drill-down thinking
- Data-quality validation before analysis
- Communicating assumptions and limitations clearly

## Business problems solved

The project demonstrates a repeatable approach for answering questions such as which products need replenishment review, which products carry excess or non-moving stock, which batches need expiry attention, and which categories hold the most inventory value or operational risk.

The public project does not claim to reproduce any specific organization's policy. Thresholds are generalized portfolio assumptions and can be changed by a business owner.

## Technologies used

- HTML5, CSS3, Vanilla JavaScript
- Python 3 standard library
- SQL
- Power BI / DAX design documentation
- GitHub Actions
- GitHub Pages compatible static hosting

## Points I can discuss during an interview

### Business-analysis discussion

- How I converted a broad stock-management problem into specific decision questions.
- Why recent sales and stock quantity alone are not enough without expiry and stock-cover context.
- How business thresholds should be configurable and approved by the relevant operational owner.
- Why dead stock, slow-moving stock, and expiry risk are different problems and should not be collapsed into one flag.

### Data-model discussion

- Why stock is modeled at batch level while products are modeled at SKU level.
- Why sales are retained at daily grain even when the primary KPI uses a 90-day window.
- How a one-to-many relationship from product to sales and stock batches prevents duplicated product attributes.

### Analytical-method discussion

- Stock Cover Days = On-hand Stock / Average Daily Units Sold.
- Why zero-sales SKUs need special treatment instead of division by zero.
- Why reorder logic should ideally incorporate supplier lead time, safety stock, service levels, and open purchase orders in a production model.
- Why retail inventory value is a portfolio simplification and should not be confused with accounting inventory cost.

### Dashboard discussion

- Why I used global filters plus action-oriented tables.
- Why the top layer shows executive KPIs while the lower layer shows operational candidates.
- How the same model can be implemented in Power BI for enterprise deployment.

### Privacy / governance discussion

- I replaced operational data with deterministic synthetic datasets before publication.
- I separated demonstration logic from organization-specific business rules.
- I included automated validation for common PII/secrets patterns and documented the publication checklist.

## Limitations I would state in an interview

- The repository uses synthetic data; therefore it demonstrates the method, not a real company's performance.
- The reorder formula is intentionally simplified and does not include supplier lead time, open orders, minimum order quantities, service-level targets, or cost constraints.
- Inventory valuation uses retail price because unit cost is not part of the public synthetic model.
- A production solution would require business-owned thresholds, role-based access, scheduled refresh, auditability, and formal data governance.
