# Environment Baseline

## Browser runtime

The dashboard uses:

- HTML5
- CSS3
- Vanilla JavaScript
- local synthetic CSV files

There is no front-end package-install step.

Run locally:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Python

Recommended:

- Python 3.10+
- GitHub Actions: Python 3.12
- core data generator: Python standard library
- optional test dependency: pytest 8.x

## SQLite

The SQL scripts are written for SQLite-compatible execution.

They use constructs such as:

- `PRAGMA foreign_keys = ON`
- `date(...)`
- SQLite-compatible DDL and analytical queries

## Power BI

Power BI documentation is implementation guidance only. No source-controlled Power BI runtime artifact is committed.

## Deployment

GitHub Pages publishes the static dashboard through `.github/workflows/deploy-pages.yml`.
