# Contributing

This repository is primarily a portfolio demonstration, but improvements are welcome.

## Development workflow

1. Create a feature branch.
2. Keep all public datasets synthetic.
3. Do not add credentials, personal data, real customer/employee/prescription records, proprietary datasets, or internal infrastructure information.
4. Run `python scripts/validate_repository.py`.
5. Run `python -m pytest -q` if pytest is installed.
6. Update documentation when KPI logic or assumptions change.
7. Open a pull request with a concise business and technical explanation.

## Code style

Prefer clear, dependency-light implementations. KPI logic should be explainable and documented rather than hidden in UI code.
