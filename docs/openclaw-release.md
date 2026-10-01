# OpenClaw and ClawHub Release Guide

## Two independent packages

Publish each skill directory as its own ClawHub package. Do not upload the whole source repository as one skill. Keep the existing slugs so prompts and installed references remain stable.

| Package slug | Display name | Package root |
| --- | --- | --- |
| `zhizhi-math-coach` | Zhizhi Math Coach | `skills/zhizhi-math-coach/` |
| `zhizhi-math-worksheet` | Zhizhi Math Worksheets | `skills/zhizhi-math-worksheet/` |

Suggested English listing summaries:

- **Coach:** Check elementary math work, explain mistakes, document full papers, and track learning evidence. Includes optional OpenClaw background processing and personal-repository sync. Archive helpers currently favor Chinese-school workflows.
- **Worksheets:** Turn a worksheet photo or question list into printable math practice with separate answers and page previews. Keep a full-paper variant workflow or use selected questions for review. English and Chinese output instructions; no learning archive or GitHub setup required.

The worksheet skill does not depend on the coach package. It needs an agent with appropriate image understanding when using photos, local document-authoring tools, and a PDF renderer for preview checks. It does not bundle a model, image-generation API, or document runtime. Coach integration is optional; if the worksheet skill is absent, the coach retains its existing compatibility workflow. This repository ships skills, not an OpenClaw plugin tool package.

## Language and regional support

English is the canonical language of public skill descriptions, UI metadata, and the worksheet's runtime references. `README.md` is the English project guide; `README.zh-CN.md` remains the Chinese guide. Do not package duplicate executable skills solely to translate their descriptions.

Output language is independent of instruction language: follow explicit student/parent language preferences, otherwise retain the source language for student material and use the conversation language for explanations. Default to A4 unless another paper size is requested. Do not infer curriculum, currency, units, timezone, or school dates from language.

Current limits must be visible in release notes:

- The coach's initializer, some archive summaries, and legacy question templates still use Chinese labels and Chinese-school defaults. They are not completely localized.
- English model-authored HTML has English generated answer headings and explanations; this does not automatically translate supplied question content.
- The reviewed PDF samples are Chinese. English HTML/answer checks do not substitute for English PDF visual testing or tests of another national curriculum.
- Existing generation examples are not controlled evidence of improved learner outcomes.

## Package checks

From the repository root:

```bash
python3 -B scripts/smoke_check.py
python3 -B -m unittest discover -s tests -v
```

Also validate both skill folders with the available skill validator. Check that each package has matching folder/frontmatter identity and that its required references are inside that package. The worksheet package should remain usable without sibling package files or root-level README files.

Include only maintained skill instructions, referenced docs, scripts, assets, and synthetic examples appropriate to that package. Keep real student records, completed work, school papers, source photos, textbook copies, generated PDFs/previews, local caches, and credentials out of ClawHub bundles. Inspect each selected package directory before upload; a clean root `.gitignore` is not a package-content check.

## Install and behavior checks

Use an isolated personal workspace and install the package being checked by itself. For the worksheet package, try:

```text
$zhizhi-math-worksheet Make a similar version of this worksheet for A4 printing, with separate answers.
$zhizhi-math-worksheet Create variants from this question list in English, with an English answer key.
$zhizhi-math-worksheet Typeset these questions without changing their numbers or wording.
$zhizhi-math-worksheet Keep the student paper in Chinese and explain the answers to me in English.
```

Confirm the two input branches, correct language selection, source-to-output mappings, separate solutions, available-runtime handling, and actual PDF rendering. The full-paper path must not require the question-list format first. Do not describe installation or a live OpenClaw run as tested unless it was performed.

For the coach, test grading, full-paper records, uncertainty, and a supplied regional profile before enabling scheduled jobs or synchronization. A request to generate a worksheet must not silently enable those services.

## Publication and versions

Use the current ClawHub CLI or website to publish the selected package root under its matching slug, with a new package version and English release notes. Follow the current CLI help for exact options. Prepare the files and checks before requesting any final publication approval if required. Local changes or validation do not mean the package has been published. Updating one package does not imply that the other was released.

## Optional GitHub Pages

Pages is a separate feature for a personal learning repository. It is not part of ClawHub installation. Publish only child-facing worksheet files, using the coach's configured authorization and publication workflow when available; keep answers and learning records private. A local printable worksheet is a valid result without GitHub or Pages.
