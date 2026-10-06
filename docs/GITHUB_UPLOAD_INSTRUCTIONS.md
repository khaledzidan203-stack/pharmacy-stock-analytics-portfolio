# Repository Setup and Publication

This repository is already configured for GitHub-based validation and static dashboard deployment.

## Local validation

Before pushing changes, run:

```bash
python scripts/validate_repository.py
python scripts/check_reproducibility.py
python -m pytest -q
node --check src/js/app.js
```

## GitHub Pages

The repository includes:

`.github/workflows/deploy-pages.yml`

The workflow deploys the static dashboard from the repository to GitHub Pages.

If Pages is not already enabled:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, select **GitHub Actions**.
3. Push to `main` or run the deployment workflow manually.
4. Confirm the deployment job succeeds.

## Publication safety

Before every public release:

- keep data synthetic;
- do not add production exports;
- do not add credentials or internal infrastructure details;
- review staged changes;
- confirm analytical and reproducibility tests pass.

The repository name contains `portfolio` for continuity, but project documentation presents the implementation as an independent analytical system rather than recruitment material.
