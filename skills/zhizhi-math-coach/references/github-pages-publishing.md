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
