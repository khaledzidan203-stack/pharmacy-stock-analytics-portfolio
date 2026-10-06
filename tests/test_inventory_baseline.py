from __future__ import annotations

import csv
import math
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DATE = date(2026, 8, 26)


def rows(name: str) -> list[dict[str, str]]:
    with (ROOT / "data" / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_committed_dataset_shape_and_window():
    products = rows("sample_products.csv")
    sales = rows("sample_sales_90_days.csv")
    batches = rows("sample_stock_batches.csv")
    snapshot = rows("sample_inventory_snapshot.csv")

    assert len(products) == 120
    assert len(sales) == 10800
    assert len(batches) == 231
    assert len(snapshot) == 120

    dates = sorted({r["date"] for r in sales})
    assert len(dates) == 90
    assert dates[0] == "2026-05-29"
    assert dates[-1] == "2026-08-26"

    assert len({r["product_id"] for r in products}) == 120
    assert len({r["item_code"] for r in products}) == 120


def test_committed_aggregate_kpi_baseline():
    snapshot = rows("sample_inventory_snapshot.csv")

    assert sum(int(r["stock_qty"]) > 0 for r in snapshot) == 114
    assert sum(int(r["stock_qty"]) for r in snapshot) == 10682
    assert math.isclose(
        sum(float(r["inventory_value_sar"]) for r in snapshot),
        737970.61,
        abs_tol=1e-6,
    )
    assert sum(int(r["sales_90d_qty"]) for r in snapshot) == 16337
    assert math.isclose(
        sum(float(r["sales_value_90d_sar"]) for r in snapshot),
        1245983.10,
        abs_tol=1e-6,
    )
    assert sum(int(r["expired_units"]) for r in snapshot) == 472
    assert sum(int(r["units_expiring_30d"]) for r in snapshot) == 1050
    assert sum(int(r["dead_stock_flag"]) for r in snapshot) == 9
    assert math.isclose(
        sum(
            float(r["inventory_value_sar"])
            for r in snapshot
            if int(r["dead_stock_flag"]) == 1
        ),
        8041.23,
        abs_tol=1e-6,
    )
    assert sum(int(r["slow_moving_flag"]) for r in snapshot) == 16
    assert sum(int(r["reorder_candidate_flag"]) for r in snapshot) == 26
    assert sum(int(r["reorder_qty_30d"]) for r in snapshot) == 929


def test_snapshot_reconciles_to_products_sales_and_batches():
    products = {int(r["product_id"]): r for r in rows("sample_products.csv")}
    sales_by_product: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows("sample_sales_90_days.csv"):
        sales_by_product[int(row["product_id"])].append(row)

    batches_by_product: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows("sample_stock_batches.csv"):
        batches_by_product[int(row["product_id"])].append(row)

    for row in rows("sample_inventory_snapshot.csv"):
        pid = int(row["product_id"])
        product = products[pid]
        price = float(product["retail_price_sar"])

        sales_rows = sales_by_product[pid]
        sales_qty = sum(int(r["quantity"]) for r in sales_rows)
        sales_value = round(sum(float(r["sales_value_sar"]) for r in sales_rows), 2)

        batch_rows = batches_by_product[pid]
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

        assert row["item_code"] == product["item_code"]
        assert row["category"] == product["category"]
        assert row["sub_category"] == product["sub_category"]
        assert math.isclose(float(row["retail_price_sar"]), price, abs_tol=1e-9)

        assert int(row["stock_qty"]) == stock_qty
        assert int(row["sales_90d_qty"]) == sales_qty
        assert math.isclose(float(row["sales_value_90d_sar"]), sales_value, abs_tol=1e-6)
        assert math.isclose(float(row["avg_daily_units"]), round(avg, 3), abs_tol=1e-9)
        assert math.isclose(
            float(row["inventory_value_sar"]),
            round(stock_qty * price, 2),
            abs_tol=1e-6,
        )

        if cover is None:
            assert row["stock_cover_days"] == ""
        else:
            assert math.isclose(float(row["stock_cover_days"]), round(cover, 1), abs_tol=1e-9)

        assert int(row["expired_units"]) == expired_units
        assert int(row["units_expiring_30d"]) == expiring_30d
        assert row["nearest_expiry_date"] == ("" if nearest is None else nearest.isoformat())
        assert int(row["dead_stock_flag"]) == int(dead)
        assert int(row["slow_moving_flag"]) == int(slow)
        assert int(row["reorder_candidate_flag"]) == int(reorder)
        assert int(row["reorder_qty_30d"]) == reorder_qty


def test_risk_flags_are_not_forced_into_exclusive_buckets():
    snapshot = rows("sample_inventory_snapshot.csv")

    expiry_reorder = sum(
        (int(r["expired_units"]) + int(r["units_expiring_30d"]) > 0)
        and int(r["reorder_candidate_flag"]) == 1
        for r in snapshot
    )
    dead_expiry = sum(
        int(r["dead_stock_flag"]) == 1
        and (int(r["expired_units"]) + int(r["units_expiring_30d"]) > 0)
        for r in snapshot
    )
    slow_expiry = sum(
        int(r["slow_moving_flag"]) == 1
        and (int(r["expired_units"]) + int(r["units_expiring_30d"]) > 0)
        for r in snapshot
    )

    assert expiry_reorder == 7
    assert dead_expiry == 5
    assert slow_expiry == 4


def test_category_baseline():
    snapshot = rows("sample_inventory_snapshot.csv")
    by_category: dict[str, dict[str, float]] = defaultdict(lambda: {
        "inventory": 0.0,
        "expiry": 0.0,
        "dead": 0.0,
    })

    for row in snapshot:
        bucket = by_category[row["category"]]
        bucket["inventory"] += float(row["inventory_value_sar"])
        bucket["expiry"] += int(row["expired_units"]) + int(row["units_expiring_30d"])
        bucket["dead"] += int(row["dead_stock_flag"])

    assert math.isclose(by_category["OTC"]["inventory"], 298200.59, abs_tol=1e-6)
    assert by_category["OTC"]["expiry"] == 709
    assert by_category["Medical Supplies"]["dead"] == 3
    assert by_category["Medical Supplies"]["expiry"] == 302
