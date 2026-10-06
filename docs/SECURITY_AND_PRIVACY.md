# Security and Privacy

## Public-repository policy

This repository is designed around synthetic, non-production data.

### Never commit

- Customer or patient information
- Prescription information
- National IDs or other government identifiers
- Employee information
- Passwords, tokens, API keys, certificates or secret files
- Database connection strings
- Internal server names, IP addresses or private URLs
- Real commercial contracts or confidential business rules
- Proprietary operational datasets
- Raw production spreadsheets or exports

## Controls included

- `.gitignore` excludes common spreadsheet/private-data paths and environment files.
- `scripts/validate_repository.py` scans public text/CSV files for common secret and PII-like patterns.
- Synthetic data uses generic SKU codes and product names.
- Deterministic regeneration verifies public-source provenance.
- Analytical thresholds are explicitly documented as synthetic assumptions.

## Publication checklist

Before release:

```bash
python scripts/validate_repository.py
python scripts/check_reproducibility.py
python -m pytest -q
```

Then review the staged diff manually.
