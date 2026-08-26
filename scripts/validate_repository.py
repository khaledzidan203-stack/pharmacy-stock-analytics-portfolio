"""Validate public sample data and scan for common PII/secrets patterns."""
from pathlib import Path
import csv,re,sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]

def read_csv(name):
    with (ROOT/'data'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

products=read_csv('sample_products.csv'); sales=read_csv('sample_sales_90_days.csv'); batches=read_csv('sample_stock_batches.csv'); snap=read_csv('sample_inventory_snapshot.csv')
pids={r['product_id'] for r in products}
if len(pids)!=len(products):errors.append('Duplicate product_id found.')
if len({r['item_code'] for r in products})!=len(products):errors.append('Duplicate item_code found.')
if any(r['product_id'] not in pids for r in sales):errors.append('Orphan sales product reference.')
if any(r['product_id'] not in pids for r in batches):errors.append('Orphan stock product reference.')
if any(int(r['quantity'])<0 for r in sales):errors.append('Negative sales quantity.')
if any(int(r['stock_qty'])<0 for r in batches):errors.append('Negative stock quantity.')
if len(snap)!=len(products):errors.append('Snapshot row count does not match products.')

patterns={
 'possible_email':re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',re.I),
 'possible_ipv4':re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
 'possible_private_key':re.compile(r'BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY'),
 'possible_secret_assignment':re.compile(r'(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{12,}'),
 'possible_saudi_national_id_like':re.compile(r'(?<!\d)[12]\d{9}(?!\d)'),
}
text_ext={'.md','.txt','.html','.css','.js','.py','.sql','.csv','.yml','.yaml','.json'}
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in text_ext:
        text=p.read_text(encoding='utf-8',errors='ignore')
        for label,pat in patterns.items():
            if pat.search(text):
                # Documentation may name secret field types; only assignment pattern is designed to avoid prose false positives.
                if label in {'possible_email','possible_ipv4','possible_private_key','possible_secret_assignment','possible_saudi_national_id_like'}:
                    errors.append(f'{label}: {p.relative_to(ROOT)}')

if errors:
    print('VALIDATION FAILED')
    for e in sorted(set(errors)):print('-',e)
    sys.exit(1)
print(f'VALIDATION PASSED: {len(products)} synthetic products, {len(sales)} daily sales rows, {len(batches)} stock batches.')
