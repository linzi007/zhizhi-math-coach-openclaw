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

Create or clone the personal GitHub repository first, then install the skill from ClawHub and run the initializer inside that repository:

```bash
mkdir zhizhi-math-learning-data
cd zhizhi-math-learning-data
git init
openclaw skills install zhizhi-math-coach
python3 skills/zhizhi-math-coach/scripts/init_learning_workspace.py \
  --workspace . \
  --student-name "孩子" \
  --school-entry-year 2025 \
  --grade 一年级 \
  --semester 下学期 \
  --textbook-edition 人教版 \
  --textbook-volume 一年级下册
git add .
git commit -m "Initialize math learning workspace"
git remote add origin git@github.com:<user>/zhizhi-math-learning-data.git
git push -u origin main
```

Open this personal repository as the OpenClaw workspace. The generated `.gitignore` ignores `skills/` by default, so downloaded ClawHub bundles are not committed into the personal learning repository.

## GitHub Authorization On The OpenClaw Machine

Do not assume the OpenClaw machine has GitHub CLI or saved credentials. Sync requires ordinary `git` plus either SSH authorization or an HTTPS personal access token.

Preferred SSH setup:

```bash
git --version
ssh -T git@github.com
git remote set-url origin git@github.com:<user>/zhizhi-math-learning-data.git
python3 skills/zhizhi-math-coach/scripts/check_git_sync.py --workspace . --check-push
```

HTTPS token setup, when SSH is unavailable:

1. Create a fine-grained personal access token in GitHub: profile photo -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens -> Generate new token.
2. Select only the personal learning repository under repository access.
3. Grant `Contents: Read and write` for normal commit/push sync.
4. Grant `Workflows: Read and write` only if committing `.github/workflows/pages.yml`.
5. Grant `Pages: Read and write` only if automation will manage GitHub Pages through the API.
6. Set the remote to HTTPS and test push authorization:

```bash
git remote set-url origin https://github.com/<user>/zhizhi-math-learning-data.git
git push --dry-run origin HEAD
```

When Git prompts for credentials, enter the GitHub username and use the token as the password. Never paste tokens into OpenClaw chat, commit them into files, or embed them in remote URLs.

## Working Directory Rules

Use this personal repository for daily learning work:

- grading and diagnosis;
- explanation cards;
- worksheet generation;
- publishing child-facing pages;
- committing and pushing learning data.

Use `zhizhi-math-coach-openclaw/` only for reusable skill maintenance:

- editing `skills/zhizhi-math-coach/`;
- updating templates or sanitized examples;
- running `scripts/smoke_check.py`;
- preparing GitHub or ClawHub releases.

If the current directory is `zhizhi-math-coach-openclaw/`, do not run a normal student learning session there. Generated student data would be written into the reusable skill repository instead of this personal learning repository.

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

GitHub sync is explicit. Before OpenClaw commits or pushes, run:

```bash
python3 skills/zhizhi-math-coach/scripts/check_git_sync.py --workspace . --check-push
```

If authorization is missing, keep the generated local files and retry sync after SSH or token setup. In a private personal repository, use:

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

# Installed skills can be reinstalled from ClawHub.
skills/

# Optional large or sensitive raw inputs
uploads/raw/
ocr-output/raw/
textbooks/*.pdf
```

## Publish Child-Facing Worksheets

Run from the personal learning repository:

```bash
python3 skills/zhizhi-math-coach/scripts/publish_html_site.py \
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
