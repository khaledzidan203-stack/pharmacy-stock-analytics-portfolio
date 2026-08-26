# Business Requirements

## Purpose

Provide an analytical view that helps inventory stakeholders prioritize stock actions using recent sales, stock-on-hand, product category, and expiry information.

## Users

- Inventory analyst
- Category / commercial analyst
- Pharmacy operations reviewer
- Business analyst / management reviewer

## Core questions

1. What is the current stock quantity and retail value?
2. Which products have low cover relative to recent demand?
3. Which products are slow moving or have zero recent sales?
4. Which stock is expired or approaching expiry?
5. Which categories concentrate inventory value or risk?
6. What records fail basic data-quality rules?

## Functional requirements

- Filter the analysis by category and subcategory.
- Provide action-oriented stock views: reorder, expiry, dead stock, slow moving.
- Show KPI cards and category-level visual summaries.
- Provide SKU-level candidate tables for review.
- Keep KPI definitions documented and reproducible.
- Use synthetic data in the public repository.

## Non-functional requirements

- Runs as a static website through a local HTTP server or GitHub Pages.
- No credentials or back-end service required.
- No external JavaScript framework required.
- Logic must be readable and explainable to a reviewer.

## Out of scope for the public demo

- Production ERP/POS integration
- Purchase-order automation
- Prescription/customer data
- Real supplier contracts or lead times
- Accounting inventory valuation
- Organization-specific policy thresholds
