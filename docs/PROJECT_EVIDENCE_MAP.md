# Project Evidence Map

| Claim | Primary evidence | Evidence type |
|---|---|---|
| Fixed seed 20260826 | `scripts/generate_sample_data.py` | Source code |
| 120 SKUs | product CSV + tests | Data + automated check |
| 10,800 daily sales rows | sales CSV + tests | Data + automated check |
| 231 stock batches | stock-batch CSV + tests | Data + automated check |
| 90-day window | sales CSV + tests | Data + automated check |
| 10,682 stock units | inventory snapshot + tests | Derived data + automated check |
| SAR 737,970.61 inventory retail value | snapshot + tests | Derived data + automated check |
| 16,337 90-day sales units | snapshot + tests | Derived data + automated check |
| SAR 1,245,983.10 sales value | snapshot + tests | Derived data + automated check |
| 472 expired units | snapshot + tests | Derived data + automated check |
| 1,050 expiring ≤30d units | snapshot + tests | Derived data + automated check |
| 9 dead-stock SKUs | snapshot + tests | Derived data + automated check |
| 16 slow-moving SKUs | snapshot + tests | Derived data + automated check |
| 26 reorder candidates | snapshot + tests | Derived data + automated check |
| 929 suggested replenishment units | snapshot + tests | Derived data + automated check |
| Implemented browser dashboard | `index.html`, `src/`, screenshot | Runtime artifact |
| SQLite-compatible analytical layer | `sql/*.sql` | SQL source |
| GitHub Pages deployment | `.github/workflows/deploy-pages.yml` | Deployment workflow |
| Power BI runtime model | No PBIX/PBIP/PBIR/TMDL committed | **Not claimed** |
| Power BI design | `docs/POWER_BI_GUIDE.md` | Blueprint |
| Accounting inventory value | Retail price is used, not governed cost | **Not claimed** |

## Evidence rule

The presentation infographic under `docs/assets/` is a schematic summary. Exact categories, calculations, runtime status and values are governed by the committed synthetic data, executable source, tests, SQL files and retained dashboard screenshot.
