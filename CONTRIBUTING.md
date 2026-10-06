# Contributing

Improvements are welcome as long as the repository remains reproducible, synthetic, and analytically transparent.

## Development workflow

1. Create a feature branch.
2. Keep all public datasets synthetic.
3. Do not add credentials, personal data, real customer/employee/prescription records, proprietary datasets, or internal infrastructure information.
4. Run `python scripts/validate_repository.py`.
5. Run `python scripts/check_reproducibility.py`.
6. Run `python -m pytest -q`.
7. Update documentation whenever KPI logic, assumptions, or evidence boundaries change.
8. Open a pull request with a concise business and technical explanation.

## Code style

Prefer clear, dependency-light implementations. KPI logic should remain explainable, testable, and documented rather than being hidden only inside UI code.
