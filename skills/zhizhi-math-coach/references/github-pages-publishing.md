# GitHub Pages Publishing

## Purpose

Use GitHub Pages for child-facing worksheet HTML when the parent accepts public worksheet links.

Do not publish answers, diagnosis records, long-term memory, weak-point history, student photos, school papers, or textbook files.

## Default Flow

After generating a worksheet:

```bash
python3 {baseDir}/scripts/publish_html_site.py \
  worksheets/YYYY-MM-DD-topic \
  --workspace <private-learning-workspace> \
  --base-url https://<github-user>.github.io/<repo>
```

The publisher writes:

- `site/index.html`: public worksheet list.
- `site/worksheets/<slug>/index.html`: child-facing worksheet page.
- `site/.nojekyll`: disables Jekyll processing.
- `worksheets/YYYY-MM-DD-topic/publish.json`: publication manifest.

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

When Pages is configured, return the Pages URL to the parent and use it in Feishu notifications. Keep answer keys and diagnosis links private.
