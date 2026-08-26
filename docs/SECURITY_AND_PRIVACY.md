# Security and Privacy

## Public-repository policy

This repository is designed to be safe for public portfolio use.

### Never commit

- Customer or patient information
- Prescription information
- National IDs or other government identifiers
- Employee information
- Passwords, tokens, API keys, certificates, or secret files
- Database connection strings
- Internal server names, IP addresses, or private URLs
- Real commercial contracts or confidential business rules
- Proprietary operational datasets
- Raw Excel exports from production systems

## Controls included

- `.gitignore` excludes common spreadsheet/private-data paths and environment files.
- `scripts/validate_repository.py` scans public text/CSV files for common secret and PII patterns.
- Synthetic data uses generic SKU codes and product names.
- Organization-specific thresholds are generalized as portfolio assumptions.

## Publication checklist

Before pushing a new version:

```bash
python scripts/validate_repository.py
```

Also manually review `git diff --staged` before each commit.
