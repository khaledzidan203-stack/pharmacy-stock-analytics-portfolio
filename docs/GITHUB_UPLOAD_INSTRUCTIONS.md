# GitHub Upload Instructions

## Option 1 — Git command line

1. Create a new empty GitHub repository, for example `pharmacy-stock-analytics-portfolio`.
2. Do **not** add a README, `.gitignore`, or license on GitHub because they already exist locally.
3. From the project folder run:

```bash
git init
git add .
git status
git commit -m "Initial portfolio release: pharmacy inventory analytics"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/pharmacy-stock-analytics-portfolio.git
git push -u origin main
```

## Option 2 — GitHub web upload

1. Create a new empty repository.
2. Open **Add file → Upload files**.
3. Drag the **contents** of the unzipped project folder into the upload area.
4. Confirm that `.github`, `data`, `docs`, `src`, `sql`, `scripts`, `examples`, `screenshots`, and `tests` are included.
5. Commit the files to `main`.

## Enable GitHub Pages

The repository includes an optional GitHub Actions Pages workflow.

1. Open **Settings → Pages**.
2. Under **Build and deployment**, choose **GitHub Actions**.
3. Open the **Actions** tab.
4. Select **Deploy Dashboard to GitHub Pages** and click **Run workflow**.
5. Confirm the workflow completes successfully.
6. GitHub will show the published site URL in the deployment result.

If you do not want to publish a live dashboard, disable or remove `.github/workflows/deploy-pages.yml`.

## Final check before publication

Run locally:

```bash
python scripts/validate_repository.py
```

Then review:

```bash
git diff --cached
```

Never upload a private/raw data export to the public repository.
