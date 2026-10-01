# Changelog

## Unreleased

- Clarified coach/worksheet companion identities, same-agent handoff and return, and existing-install update instructions for paired coach `0.3.1` and worksheet `0.1.1` releases.
- Prepared English skill discovery text, worksheet references, prompts and separate ClawHub package guidance; added explicit output-language/curriculum rules and English model-HTML answer labels with a sanitized sample, while documenting remaining Chinese archive defaults.
- Added standalone `zhizhi-math-worksheet` with full-paper photo and general question-list branches, separate answer PDFs and optional diagnostic context from the coach; documented reviewed list/diagram examples and the remaining learning-outcome validation limits.
- Documented photo-to-variant generation with direct model-authored PDF layouts, reference-aware typography, separate printable answers and content/preview review, alongside the HTML generator.
- Added model-authored worksheets with a shared A4 print profile, separate answer manifests and optional PDF page previews; fixed templates remain optional.

- Added full-paper photo archives with original images, all visible item results and structured JSON evidence.
- Added evidence-based knowledge-point assessment, spaced-review suggestions and automatic light/full recording decisions.
- Added a durable leased photo queue and an opt-in OpenClaw cron consumer every five minutes.
- Made local recording idempotent and recoverable after partial writes; added read-only dry runs and path/date checks.
- Added clocks, number lines, shape collections, shaded grids and polygons; visual practice templates verify answers against diagram data.
- Fixed scoped Git commits, selected-only publishing, generation-time semantic validation and post-rebase deployment tracking.
- Added local regression tests for recording, photo jobs, assessments, rendering and Git/publication boundaries.

- Renamed the public skill identity to `zhizhi-math-coach`.
- Added China grade, semester, exam, and holiday planning references.
- Added curriculum and textbook-scope alignment guidance.
- Added knowledge-point explanation card guidance.
- Added worksheet strategy guidance for wrong-question variants, weak-point drills, exam review, relapse repair, spaced review, transfer checks, diagnostics, and geometry.
- Added deterministic `geometry_problem` rendering through structured SVG specs.
- Added complex word-problem item types and worksheet spec validation.
- Added OpenClaw automation and plugin-tool roadmap docs.
- Added GitHub Pages publishing for child-facing worksheet HTML.
- Added GitHub sync authorization guidance and a plain-git preflight checker.
- Added repository Deploy key setup guidance for OpenClaw environments without GitHub token configuration.
- Added public-repository GitHub Pages guidance and a workflow setup helper.
- Updated the public worksheet index to list all worksheets by date with practice status and summary columns.
- Added automatic Pages publish/push/wait helper for generated worksheets.
- Added an OpenClaw quickstart reference and clearer README first-use guidance.
- Clarified the future plugin roadmap as a stable execution layer around the Skill.
- Added PDF-first worksheet delivery: the generator writes `worksheet.pdf` when Chrome/Chromium is available, and Pages publishing can include the PDF.
- Added explicit GitHub advanced-setup trigger phrases and a public Chinese setup guide for cloud sync and Pages.
- Added fast daily grading workflow with compact active context, diagnosis payload validation, run logging, subagent boundaries, and deferred grading push support.
