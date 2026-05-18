# OpenClaw Release Notes

## Skill Identity

- Public skill name: `zhizhi-math-coach`
- Main entry: `$zhizhi-math-coach`
- Skill path: `skills/zhizhi-math-coach`

## V1 Scope

V1 is a Skill-first release. It supports:

- grading and diagnosis;
- weak-point tracking;
- parent explanations and student summaries;
- China grade/semester/calendar alignment;
- curriculum and textbook-scope references;
- worksheet generation from JSON specs;
- deterministic geometry SVG rendering for simple diagrams;
- GitHub Pages publishing for public child-facing worksheet HTML;
- validation and smoke checks.

V1 does not ship an OpenClaw plugin tool package. Plugin interfaces are documented in `docs/plugin-tools-roadmap.md`.

## Pre-release Checklist

Run from the repository root:

```bash
python3 scripts/smoke_check.py
```

Check manually:

- `README.md` uses `zhizhi-math-coach`.
- `SKILL.md` frontmatter name is `zhizhi-math-coach`.
- no real student data, school papers, PDFs, images, screenshots, or OCR dumps are committed;
- sample worksheets are sanitized;
- examples do not copy textbook problem sets.

## Install Test

Open this repository as an OpenClaw workspace, then try:

```text
$zhizhi-math-coach 批改这几道错题，并记录薄弱项。
$zhizhi-math-coach 根据退位减法薄弱项出一张练习卷。
$zhizhi-math-coach 给家长一份周长知识点讲解稿。
```

For ClawHub publication, package only reusable skill files, docs, scripts, and sanitized examples.

## GitHub Pages

To publish the public demo worksheets, enable Pages in repository settings and choose GitHub Actions as the source. The workflow deploys the committed `site/` directory only.
