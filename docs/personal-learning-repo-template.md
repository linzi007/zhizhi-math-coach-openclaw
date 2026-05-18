# Personal Learning Repository Template

Use a separate personal learning repository for each family's generated learning data. That repository may be public or private; the user chooses based on their sharing and privacy needs. This public repository only provides the reusable OpenClaw skill, scripts, templates, and sanitized examples.

## Recommended Layout

```text
zhizhi-math-learning-data/
  README.md
  .gitignore
  .github/workflows/pages.yml
  curriculum/
  knowledge-points/
  memory/
  mistakes/
  records/
  weak-points/
  worksheets/
  site/
```

## Initialize

```bash
mkdir zhizhi-math-learning-data
cd zhizhi-math-learning-data
git init
cp -R /path/to/zhizhi-math-coach-openclaw/examples/student-workspace/* .
git add .
git commit -m "Initialize math learning workspace"
git remote add origin git@github.com:<user>/zhizhi-math-learning-data.git
git push -u origin main
```

Open this personal repository as the OpenClaw workspace. Install or reference the reusable `zhizhi-math-coach` skill from the public repository.

## Trigger Model

OpenClaw does not automatically sync this repository in the background.

Local updates happen when OpenClaw is opened in this personal repository and the user invokes the reusable skill:

```text
$zhizhi-math-coach 批改这张练习卷，记录薄弱项。
$zhizhi-math-coach 根据最近错题生成变式练习。
```

The skill may write:

- `records/`, `mistakes/`, `weak-points/`, and `memory/` after grading or diagnosis;
- `worksheets/<date-topic>/` after worksheet generation;
- `site/` and `worksheets/<date-topic>/publish.json` after publishing child-facing HTML.

GitHub sync is explicit. In a private personal repository, use:

```bash
git add curriculum knowledge-points memory mistakes records weak-points worksheets site
git commit -m "Update learning records"
git push
```

In a public personal repository, only commit files that are safe to expose. Usually that means `site/` only, or sanitized worksheet files without answers, student identifiers, photos, uploads, or textbook-derived raw material.

## Suggested `.gitignore`

```gitignore
.DS_Store
*.log
__pycache__/
*.pyc
.venv/
venv/
.idea/

# Optional large or sensitive raw inputs
uploads/raw/
ocr-output/raw/
textbooks/*.pdf
```

## Publish Child-Facing Worksheets

Run from the personal learning repository:

```bash
python3 /path/to/zhizhi-math-coach-openclaw/skills/zhizhi-math-coach/scripts/publish_html_site.py \
  worksheets \
  --workspace . \
  --base-url https://<user>.github.io/zhizhi-math-learning-data
```

Only child-facing `worksheet.html` files are copied into `site/`. Answers, records, memories, weak-point histories, uploaded papers, and textbook files must stay out of `site/`. If the repository is public, treat everything outside `site/` as potentially visible too and only commit data you are comfortable publishing.

## Optional GitHub Pages Workflow

If you want GitHub Actions to deploy `site/`, add this to the personal learning repository as `.github/workflows/pages.yml`:

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: ["main"]
    paths:
      - "site/**"
      - ".github/workflows/pages.yml"
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "site"
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

In GitHub repository Settings -> Pages, choose GitHub Actions as the deployment source.
