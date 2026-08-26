"""Regenerate the public synthetic datasets.

No operational/private source file is read by this script.
"""
from pathlib import Path
from datetime import date, timedelta
import random, math, csv

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'
ANALYSIS_DATE=date(2026,8,26)
START=ANALYSIS_DATE-timedelta(days=89)
random.seed(20260826)
CATS={
 'OTC':['Pain & Fever','Cold & Allergy','Digestive Care'],
 'Vitamins & Wellness':['Multivitamins','Minerals','Wellness Support'],
 'Personal Care':['Oral Care','Hair Care','Hygiene'],
 'Skin Care':['Moisturizers','Cleansers','Sun Care'],
 'Baby Care':['Nutrition','Diapers & Hygiene','Accessories'],
 'Medical Supplies':['First Aid','Monitoring','Consumables']}
VEL={'OTC':1.9,'Vitamins & Wellness':1.2,'Personal Care':1.0,'Skin Care':0.8,'Baby Care':1.1,'Medical Supplies':0.7}

def poisson(lam):
    if lam<=0:return 0
    if lam<20:
        L=math.exp(-lam);k=0;p=1.0
        while p>L:k+=1;p*=random.random()
        return k-1
    return max(0,int(round(random.gauss(lam,math.sqrt(lam)))))

def dump(name, rows, fields):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
    products=[]; names=list(CATS)
    for i in range(1,121):
        cat=names[(i-1)%len(names)]; sub=CATS[cat][(i-1)//len(names)%3]
        price=round(random.uniform(8,160),2)
        base=max(.05,random.lognormvariate(math.log(VEL[cat]),.65))
        if random.random()<.14:base=0
        products.append({'product_id':i,'item_code':f'SKU-{10000+i}','product_name':f'{cat} Sample Product {i:03d}','category':cat,'sub_category':sub,'retail_price_sar':price,'base_velocity':base})
    sales=[]
    for p in products:
        for n in range(90):
            d=START+timedelta(days=n); weekend=1.12 if d.weekday() in (4,5) else 1; trend=.92+.16*n/89; q=poisson(p['base_velocity']*weekend*trend)
            sales.append({'date':d.isoformat(),'product_id':p['product_id'],'item_code':p['item_code'],'quantity':q,'sales_value_sar':round(q*p['retail_price_sar'],2)})
    sby={p['product_id']:0 for p in products}
    for r in sales:sby[r['product_id']]+=r['quantity']
    batches=[]
    for p in products:
        s90=sby[p['product_id']]
        total=random.choice([0,0,4,7,12,18,25]) if s90==0 else max(0,int(round((s90/90)*random.choice([8,12,18,30,45,75,120,180])+random.uniform(-2,4))))
        if not total:continue
        bc=1 if total<7 else random.choice([1,2,2,3]); rem=total; parts=[]
        for b in range(bc):
            q=rem if b==bc-1 else random.randint(1,max(1,rem-(bc-b-1)));parts.append(q);rem-=q
        for b,q in enumerate(parts,1):
            r=random.random()
            if r<.05:exp=ANALYSIS_DATE-timedelta(days=random.randint(1,45))
            elif r<.18:exp=ANALYSIS_DATE+timedelta(days=random.randint(1,30))
            elif r<.34:exp=ANALYSIS_DATE+timedelta(days=random.randint(31,90))
            else:exp=ANALYSIS_DATE+timedelta(days=random.randint(91,730))
            batches.append({'batch_id':f'B-{p["product_id"]:04d}-{b:02d}','product_id':p['product_id'],'item_code':p['item_code'],'expiry_date':exp.isoformat(),'stock_qty':q})
    stock={p['product_id']:0 for p in products}; ex={p['product_id']:0 for p in products}; e30={p['product_id']:0 for p in products}; near={p['product_id']:None for p in products}
    for b in batches:
        pid=b['product_id']; q=b['stock_qty']; ed=date.fromisoformat(b['expiry_date']); stock[pid]+=q
        if ed<ANALYSIS_DATE:ex[pid]+=q
        elif ed<=ANALYSIS_DATE+timedelta(days=30):e30[pid]+=q
        if near[pid] is None or ed<near[pid]:near[pid]=ed
    snap=[]
    for p in products:
        pid=p['product_id']; s90=sby[pid]; st=stock[pid]; avg=s90/90; cover=None if avg==0 else st/avg
        dead=st>0 and s90==0; slow=st>0 and s90>0 and cover>120; reorder=s90>0 and cover<14
        snap.append({'product_id':pid,'item_code':p['item_code'],'product_name':p['product_name'],'category':p['category'],'sub_category':p['sub_category'],'retail_price_sar':p['retail_price_sar'],'stock_qty':st,'sales_90d_qty':s90,'sales_value_90d_sar':round(s90*p['retail_price_sar'],2),'avg_daily_units':round(avg,3),'stock_cover_days':'' if cover is None else round(cover,1),'inventory_value_sar':round(st*p['retail_price_sar'],2),'expired_units':ex[pid],'units_expiring_30d':e30[pid],'nearest_expiry_date':'' if near[pid] is None else near[pid].isoformat(),'dead_stock_flag':int(dead),'slow_moving_flag':int(slow),'reorder_candidate_flag':int(reorder),'reorder_qty_30d':max(0,math.ceil(avg*30-st)) if reorder else 0})
    dump('sample_products.csv',[{k:v for k,v in p.items() if k!='base_velocity'} for p in products],['product_id','item_code','product_name','category','sub_category','retail_price_sar'])
    dump('sample_sales_90_days.csv',sales,['date','product_id','item_code','quantity','sales_value_sar'])
    dump('sample_stock_batches.csv',batches,['batch_id','product_id','item_code','expiry_date','stock_qty'])
    dump('sample_inventory_snapshot.csv',snap,list(snap[0]))
    print('Synthetic data regenerated successfully.')
if __name__=='__main__':main()
