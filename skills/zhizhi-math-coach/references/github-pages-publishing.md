# GitHub Pages Publishing

## Purpose

Use GitHub Pages for child-facing worksheet HTML when the parent accepts public worksheet links.

Do not publish answers, diagnosis records, long-term memory, weak-point history, student photos, school papers, or textbook files.

## Default Flow

After generating a worksheet:

```bash
python3 {baseDir}/scripts/publish_html_site.py \
  worksheets/YYYY-MM-DD-topic \
  --workspace <personal-learning-workspace> \
  --base-url https://<github-user>.github.io/<repo>
```

The publisher writes:

- `site/index.html`: public worksheet list.
- `site/worksheets/<slug>/index.html`: child-facing worksheet page.
- `site/.nojekyll`: disables Jekyll processing.
- `worksheets/YYYY-MM-DD-topic/publish.json`: publication manifest.

This only produces local `site/` files. A public URL requires the personal learning repository to be pushed to GitHub and GitHub Pages to be configured for that repository.

## Public Repository Mode

If the parent chooses to make the personal learning repository public to avoid paid private Pages:

- Clarify that the whole public repository is viewable, not only the Pages site. Public Pages makes `site/` easy to open, but GitHub users can also browse tracked files outside `site/`.
- Use this mode only when the parent accepts public visibility of committed files, or when the repository commits only public-safe files.
- Do not add collaborators unless they should be able to push.
- For `main`, public GitHub repositories are read-only to non-collaborators by default. Recommend branch protection/rulesets to block force pushes and branch deletion. Do not enable a rule that requires pull requests or blocks direct pushes if OpenClaw is expected to push `site/` and workflow updates directly.

Recommended manual GitHub setting:

1. Repository Settings -> Pages.
2. Build and deployment -> Source: `GitHub Actions`.
3. If not present, create `.github/workflows/pages.yml` with the bundled setup script:

```bash
python3 {baseDir}/scripts/setup_github_pages_workflow.py \
  --workspace <personal-learning-workspace>
```

If GitHub sync is already authorized through the Deploy key, OpenClaw may commit and push this workflow after the parent asks it to set up Pages:

```bash
git add .github/workflows/pages.yml site
git commit -m "Configure GitHub Pages publishing"
git push
```

The push triggers the GitHub Actions Pages deployment. Return the expected URL `https://<github-user>.github.io/<repo>/` and tell the parent that the first deployment may take a short time.

## Public Content Rule

Allowed in `site/`:

- child-facing worksheet HTML;
- worksheet title, date, topic, and strategy;
- generated SVG diagrams and blank answer spaces.

Forbidden in `site/`:

- `answer-key.md`;
- answers or `answer_detail`;
- `records/`, `mistakes/`, `memory/`, `weak-points/`, `knowledge-points/`, `curriculum/`;
- completed worksheet photos, school papers, textbook PDFs, scans, or OCR output.

## OpenClaw Output Rule

When Pages is configured, return the Pages URL to the parent and use it in Feishu notifications. Keep answer keys and diagnosis links outside published `site/` output.

If the parent asks OpenClaw to sync, push, publish to GitHub, or send a public link, read `github-sync-authorization.md` first. Do not assume GitHub CLI, GitHub token environment variables, or saved credentials are available. Use the Git preflight before committing or pushing. If authorization is missing, keep the local `site/` output, generate or suggest a repository Deploy key, send the public key and GitHub Settings -> Deploy keys guidance through Lark/Feishu when available, and return the local `site/` paths.
