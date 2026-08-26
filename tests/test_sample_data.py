from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]

def rows(name):
    with (ROOT/'data'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def test_products_are_unique():
    data=rows('sample_products.csv')
    assert len(data)==len({r['product_id'] for r in data})
    assert len(data)==len({r['item_code'] for r in data})

def test_sales_references_products():
    pids={r['product_id'] for r in rows('sample_products.csv')}
    assert all(r['product_id'] in pids for r in rows('sample_sales_90_days.csv'))

def test_stock_references_products_and_is_non_negative():
    pids={r['product_id'] for r in rows('sample_products.csv')}
    batches=rows('sample_stock_batches.csv')
    assert all(r['product_id'] in pids for r in batches)
    assert all(int(r['stock_qty'])>=0 for r in batches)

def test_snapshot_matches_product_count():
    assert len(rows('sample_inventory_snapshot.csv'))==len(rows('sample_products.csv'))
