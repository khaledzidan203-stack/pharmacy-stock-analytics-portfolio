# Business Requirements

## Purpose

Provide an analytical view that helps inventory stakeholders prioritize stock actions using recent sales, stock-on-hand, product category and batch expiry information.

## Users

- Inventory analyst
- Category / commercial analyst
- Pharmacy operations reviewer
- Business analyst / management reviewer

## Core questions

1. What is current on-hand stock and its retail-value proxy?
2. Which products have low cover relative to recent demand?
3. Which products are slow moving?
4. Which stocked products have no sales in the 90-day window?
5. Which stock is already expired or approaching expiry?
6. Which categories concentrate inventory value or operational risk?
7. Which records fail core data-quality rules?

## Functional requirements

- Filter by Category and Subcategory.
- Provide action-oriented stock views: Reorder, Expiry, Dead Stock and Slow Moving.
- Show KPI cards and category-level summaries.
- Visualize the 90-day demand trend.
- Show stock-cover distribution.
- Provide SKU-level candidate tables.
- Keep KPI definitions and thresholds documented.
- Use synthetic data in the public repository.

## Non-functional requirements

- Run as a static website through a local HTTP server or GitHub Pages.
- Require no credentials or back-end service.
- Require no external JavaScript framework.
- Keep calculation logic readable and testable.
- Support deterministic recreation of the public synthetic dataset.

## Out of scope

- Production ERP/POS integration
- Automated purchase-order execution
- Customer or prescription data
- Real supplier contracts or lead times
- Accounting inventory valuation
- Organization-specific threshold policies
