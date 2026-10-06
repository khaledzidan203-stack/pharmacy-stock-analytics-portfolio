"""Validate the synthetic analytical contract and public repository boundary."""
from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
import csv
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ANALYSIS_DATE = date(2026, 8, 26)
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


products = read_csv("sample_products.csv")
sales = read_csv("sample_sales_90_days.csv")
batches = read_csv("sample_stock_batches.csv")
snapshot = read_csv("sample_inventory_snapshot.csv")

product_ids = {r["product_id"] for r in products}

if len(products) != 120:
    fail(f"Expected 120 products, found {len(products)}.")
if len(sales) != 10800:
    fail(f"Expected 10,800 sales rows, found {len(sales)}.")
if len(batches) != 231:
    fail(f"Expected 231 stock batches, found {len(batches)}.")
if len(snapshot) != 120:
    fail(f"Expected 120 snapshot rows, found {len(snapshot)}.")

dates = sorted({r["date"] for r in sales})
if len(dates) != 90 or dates[0] != "2026-05-29" or dates[-1] != "2026-08-26":
    fail(f"Unexpected 90-day sales window: {dates[0] if dates else None} to {dates[-1] if dates else None}.")

if len(product_ids) != len(products):
    fail("Duplicate product_id found.")
if len({r["item_code"] for r in products}) != len(products):
    fail("Duplicate item_code found.")
if any(r["product_id"] not in product_ids for r in sales):
    fail("Orphan sales product reference.")
if any(r["product_id"] not in product_ids for r in batches):
    fail("Orphan stock product reference.")
if any(int(r["quantity"]) < 0 for r in sales):
    fail("Negative sales quantity.")
if any(int(r["stock_qty"]) < 0 for r in batches):
    fail("Negative stock quantity.")

# Snapshot reconciliation.
product_by_id = {int(r["product_id"]): r for r in products}
sales_by_product: dict[int, list[dict[str, str]]] = defaultdict(list)
batch_by_product: dict[int, list[dict[str, str]]] = defaultdict(list)

for row in sales:
    sales_by_product[int(row["product_id"])].append(row)
for row in batches:
    batch_by_product[int(row["product_id"])].append(row)

for row in snapshot:
    pid = int(row["product_id"])
    product = product_by_id[pid]
    price = float(product["retail_price_sar"])

    sales_rows = sales_by_product[pid]
    sales_qty = sum(int(r["quantity"]) for r in sales_rows)
    sales_value = round(sum(float(r["sales_value_sar"]) for r in sales_rows), 2)

    batch_rows = batch_by_product[pid]
    stock_qty = sum(int(r["stock_qty"]) for r in batch_rows)
    expired_units = sum(
        int(r["stock_qty"])
        for r in batch_rows
        if date.fromisoformat(r["expiry_date"]) < ANALYSIS_DATE
    )
    expiring_30d = sum(
        int(r["stock_qty"])
        for r in batch_rows
        if ANALYSIS_DATE
        <= date.fromisoformat(r["expiry_date"])
        <= ANALYSIS_DATE + timedelta(days=30)
    )
    nearest = min(
        (date.fromisoformat(r["expiry_date"]) for r in batch_rows),
        default=None,
    )

    avg = sales_qty / 90
    cover = None if avg == 0 else stock_qty / avg
    dead = stock_qty > 0 and sales_qty == 0
    slow = stock_qty > 0 and sales_qty > 0 and cover > 120
    reorder = sales_qty > 0 and cover < 14
    reorder_qty = max(0, math.ceil(avg * 30 - stock_qty)) if reorder else 0

    if row["item_code"] != product["item_code"]:
        fail(f"Snapshot item_code mismatch for product {pid}.")
    if int(row["stock_qty"]) != stock_qty:
        fail(f"Snapshot stock mismatch for product {pid}.")
    if int(row["sales_90d_qty"]) != sales_qty:
        fail(f"Snapshot sales quantity mismatch for product {pid}.")
    if not math.isclose(float(row["sales_value_90d_sar"]), sales_value, abs_tol=1e-6):
        fail(f"Snapshot sales value mismatch for product {pid}.")
    if not math.isclose(float(row["avg_daily_units"]), round(avg, 3), abs_tol=1e-9):
        fail(f"Snapshot average daily units mismatch for product {pid}.")
    if not math.isclose(
        float(row["inventory_value_sar"]),
        round(stock_qty * price, 2),
        abs_tol=1e-6,
    ):
        fail(f"Snapshot inventory value mismatch for product {pid}.")

    if cover is None:
        if row["stock_cover_days"] != "":
            fail(f"Zero-sales cover should be blank for product {pid}.")
    elif not math.isclose(float(row["stock_cover_days"]), round(cover, 1), abs_tol=1e-9):
        fail(f"Snapshot stock cover mismatch for product {pid}.")

    if int(row["expired_units"]) != expired_units:
        fail(f"Expired units mismatch for product {pid}.")
    if int(row["units_expiring_30d"]) != expiring_30d:
        fail(f"30-day expiry mismatch for product {pid}.")
    if row["nearest_expiry_date"] != ("" if nearest is None else nearest.isoformat()):
        fail(f"Nearest expiry mismatch for product {pid}.")
    if int(row["dead_stock_flag"]) != int(dead):
        fail(f"Dead-stock flag mismatch for product {pid}.")
    if int(row["slow_moving_flag"]) != int(slow):
        fail(f"Slow-moving flag mismatch for product {pid}.")
    if int(row["reorder_candidate_flag"]) != int(reorder):
        fail(f"Reorder flag mismatch for product {pid}.")
    if int(row["reorder_qty_30d"]) != reorder_qty:
        fail(f"Reorder quantity mismatch for product {pid}.")

# Aggregate baseline.
expected = {
    "stocked_skus": 114,
    "stock_units": 10682,
    "sales_units": 16337,
    "expired_units": 472,
    "expiring_30d": 1050,
    "dead_skus": 9,
    "slow_skus": 16,
    "reorder_skus": 26,
    "reorder_qty": 929,
}
actual = {
    "stocked_skus": sum(int(r["stock_qty"]) > 0 for r in snapshot),
    "stock_units": sum(int(r["stock_qty"]) for r in snapshot),
    "sales_units": sum(int(r["sales_90d_qty"]) for r in snapshot),
    "expired_units": sum(int(r["expired_units"]) for r in snapshot),
    "expiring_30d": sum(int(r["units_expiring_30d"]) for r in snapshot),
    "dead_skus": sum(int(r["dead_stock_flag"]) for r in snapshot),
    "slow_skus": sum(int(r["slow_moving_flag"]) for r in snapshot),
    "reorder_skus": sum(int(r["reorder_candidate_flag"]) for r in snapshot),
    "reorder_qty": sum(int(r["reorder_qty_30d"]) for r in snapshot),
}
for key, value in expected.items():
    if actual[key] != value:
        fail(f"Aggregate baseline changed for {key}: {actual[key]} != {value}.")

inventory_value = sum(float(r["inventory_value_sar"]) for r in snapshot)
sales_value = sum(float(r["sales_value_90d_sar"]) for r in snapshot)
dead_value = sum(
    float(r["inventory_value_sar"])
    for r in snapshot
    if int(r["dead_stock_flag"]) == 1
)
if not math.isclose(inventory_value, 737970.61, abs_tol=1e-6):
    fail(f"Inventory value baseline changed: {inventory_value}.")
if not math.isclose(sales_value, 1245983.10, abs_tol=1e-6):
    fail(f"Sales value baseline changed: {sales_value}.")
if not math.isclose(dead_value, 8041.23, abs_tol=1e-6):
    fail(f"Dead-stock value baseline changed: {dead_value}.")

# Repository / presentation contract.
required_files = [
    "README.md",
    "PROJECT_NOTES.md",
    "docs/README.md",
    "docs/PROJECT_INDEX.md",
    "docs/CASE_STUDY.md",
    "docs/TECHNICAL_WALKTHROUGH.md",
    "docs/PROJECT_EVIDENCE_MAP.md",
    "docs/FINAL_RELEASE_VALIDATION.md",
    "docs/ENVIRONMENT_BASELINE.md",
    "docs/assets/Pharmacy Stock Analytics Dashboard.png",
    "screenshots/dashboard-overview.png",
    "scripts/check_reproducibility.py",
    "tests/test_inventory_baseline.py",
    "sql/01_create_schema.sql",
    "sql/02_kpi_queries.sql",
    "sql/03_inventory_risk_queries.sql",
    "sql/04_data_quality_checks.sql",
]
for rel in required_files:
    if not (ROOT / rel).exists():
        fail(f"Missing required project artifact: {rel}.")

if (ROOT / "PORTFOLIO_NOTES.md").exists():
    fail("PORTFOLIO_NOTES.md should be replaced by PROJECT_NOTES.md.")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
index = (ROOT / "index.html").read_text(encoding="utf-8")
power_bi = (ROOT / "docs/POWER_BI_GUIDE.md").read_text(encoding="utf-8")
example_kpi = (ROOT / "examples/example_kpi_snapshot.csv").read_text(encoding="utf-8")
sql_schema = (ROOT / "sql/01_create_schema.sql").read_text(encoding="utf-8")

for old in ["recruiter-friendly", "Featured Portfolio", "Skills demonstrated"]:
    if old in readme:
        fail(f"Recruitment-oriented wording remains in README: {old}.")
for old in ["DATA ANALYTICS PORTFOLIO", "Analytics Portfolio", "public portfolio"]:
    if old in index:
        fail(f"Old portfolio wording remains in index.html: {old}.")
if "Active SKUs" in example_kpi:
    fail("Example KPI file still labels stocked SKUs as Active SKUs.")
if "design guidance only" not in power_bi.lower():
    fail("Power BI runtime boundary is missing.")
if "PRAGMA foreign_keys = ON" not in sql_schema:
    fail("SQLite-compatible SQL boundary is no longer evident.")
if "Pharmacy%20Stock%20Analytics%20Dashboard.png" not in readme:
    fail("README presentation image link missing.")

hero = ROOT / "docs/assets/Pharmacy Stock Analytics Dashboard.png"
if hero.exists() and hero.stat().st_size > 2 * 1024 * 1024:
    fail("Presentation overview image exceeds the 2 MB repository cap.")

# Public-text privacy / secret scan.
patterns = {
    "possible_email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "possible_ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "possible_private_key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "possible_secret_assignment": re.compile(
        r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*[\"\']?[A-Za-z0-9_\-]{12,}"
    ),
    "possible_saudi_national_id_like": re.compile(r"(?<!\d)[12]\d{9}(?!\d)"),
}
text_ext = {".md", ".txt", ".html", ".css", ".js", ".py", ".sql", ".csv", ".yml", ".yaml", ".json"}
for path in ROOT.rglob("*"):
    if path.is_file() and path.suffix.lower() in text_ext:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in patterns.items():
            if pattern.search(text):
                fail(f"{label}: {path.relative_to(ROOT)}")

if errors:
    print("VALIDATION FAILED")
    for error in sorted(set(errors)):
        print("-", error)
    sys.exit(1)

print("PASS | deterministic synthetic data contract")
print("PASS | snapshot formula and KPI reconciliation")
print("PASS | risk-classification baseline")
print("PASS | presentation and tool-boundary contract")
print("PASS | public-text privacy / secret scan")
print("REPOSITORY VALIDATION PASS")
