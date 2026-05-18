# Worksheet Generation

## Goal

Use a compact JSON spec to avoid rewriting full HTML. The spec is the source of truth; generated files are `worksheet.html` and `answer-key.md`. When GitHub Pages publishing is enabled, the child-facing HTML can also be copied into `site/`.

## Default Flow

1. Read memory, progress, worksheet standards, and the relevant weak point.
2. For word problems, read `word-problem-variant-design.md` and write a short design note.
3. Create or update `worksheets/YYYY-MM-DD-<topic-slug>/worksheet-spec.json`.
4. Use item types from `assets/worksheet/question-types.json` when possible.
5. Validate first:

```bash
python3 {baseDir}/scripts/validate_worksheet_spec.py \
  worksheets/YYYY-MM-DD-<topic-slug>/worksheet-spec.json
```

6. Run:

```bash
python3 {baseDir}/scripts/generate_worksheet.py \
  worksheets/YYYY-MM-DD-<topic-slug>/worksheet-spec.json
```

7. If page count matters, add `--verify-print` and ensure Chrome/Chromium is installed.
8. If a public worksheet link is needed, publish child-facing HTML only:

```bash
python3 {baseDir}/scripts/publish_html_site.py \
  worksheets/YYYY-MM-DD-<topic-slug> \
  --workspace <private-learning-workspace> \
  --base-url https://<github-user>.github.io/<repo>
```

9. Reply with paths, item count, target weak point, Pages URL when available, and page count only if checked.

## Spec Rules

- Keep the spec short and structured: title, date, topic, grade, target, sections, items, grading.
- Store answers in the spec so the answer key can be regenerated.
- Add `strategy`, `diagnostic_target`, and `review_status` for generated practice.
- Keep answers out of `site/`; only publish child-facing HTML.
- Use `type` for question behavior, not surface topic. Examples: `equation`, `reading_task`, `word_problem`.
- Use `layout` for density: `grid-4`, `compact-3`, `cards-3`, `problem-grid-2`, `check-grid-2`.
- Avoid raw HTML in item data unless no existing type can express the task.
- For multi-step word problems, `answer_detail` must show intermediate values, final operation, and any unused or conditionally used information.
- For geometry, use `geometry_problem` with `geometry_spec`; do not paste AI-generated image HTML.

## Adding Question Types

When a stable new question format will recur:

1. Add an entry to `assets/worksheet/question-types.json`.
2. Add the renderer in `scripts/generate_worksheet.py`.
3. Keep fields minimal and child-action focused.
4. Regenerate the worksheet and test one sample.
5. Mention the new type name only if it matters for future reuse.

For one-off items, prefer an existing type with adjusted wording.
