# Installation

## Requirements

- Python 3.10+ recommended
- Modern browser
- Optional: pytest for automated tests

## Steps

```bash
git clone <YOUR-REPOSITORY-URL>
cd pharmacy-stock-analytics-portfolio
python -m http.server 8000
```

Open `http://localhost:8000`.

## Optional regeneration

```bash
python scripts/generate_sample_data.py
python scripts/validate_repository.py
```

## Optional tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```
