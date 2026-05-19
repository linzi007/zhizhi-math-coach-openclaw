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
- personal learning repository initialization;
- recommended model capability guidance for vision, long-context records, structured output, and reasoning effort;
- GitHub sync authorization guidance for repository Deploy keys, SSH, and fine-grained HTTPS tokens;
- Git preflight checks that do not require GitHub CLI;
- worksheet generation from JSON specs;
- deterministic geometry SVG rendering for simple diagrams;
- GitHub Pages publisher script for personal learning repositories;
- GitHub Actions Pages workflow setup for public personal repositories;
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

This public skill repository should not commit generated `site/` output. Use `publish_html_site.py` from a personal learning repository, then enable Pages in that repository if public child-facing worksheet links are acceptable. The personal learning repository may be public or private; the user chooses.

OpenClaw machines may not have GitHub CLI, credentials, or a provider-level GitHub token environment-variable setup. Prefer a repository-scoped Deploy key: generate it with `scripts/prepare_github_deploy_key.py`, send only the public key to the parent through Lark/Feishu or the OpenClaw reply, and ask the parent to add it to the personal learning repository under Settings -> Deploy keys with write access. Before any OpenClaw-initiated commit or push, run `scripts/check_git_sync.py` from the installed skill against the personal learning repository. Use a fine-grained token scoped only to the personal learning repository as a fallback.

For free GitHub Pages on a public personal repository, instruct the parent to choose Settings -> Pages -> Build and deployment -> Source: GitHub Actions. OpenClaw may create `.github/workflows/pages.yml` with `scripts/setup_github_pages_workflow.py` and push it after Git sync authorization is ready. Clarify that a public repository exposes all tracked files, not only the Pages site, while non-collaborators cannot push by default.
