# Zhizhi Math Coach OpenClaw Skill

[中文说明](README.zh-CN.md)

`zhizhi-math-coach` is an OpenClaw skill for an evidence-based primary-school math learning loop:

- grade completed worksheets, school papers, photos, or copied wrong questions;
- infer error type, likely cause, related weak point, and relapse or transfer status;
- maintain short-term memory, long-term memory, progress records, mistake books, and weak-point files;
- align practice with China grade/semester, textbook edition, school calendar, midterm/final windows, and winter/summer break;
- generate parent-facing explanations, student-readable summaries, and targeted printable worksheets;
- keep child-facing worksheets answer-free and parent-facing answer keys separate.

The repository intentionally contains only generic templates and sanitized sample data. Keep real student records, photos, school papers, textbook PDFs, and generated learning data in a separate personal learning repository.

## Project Layout

```text
skills/zhizhi-math-coach/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/init_learning_workspace.py
  scripts/generate_worksheet.py
  scripts/validate_worksheet_spec.py
  scripts/publish_html_site.py
  assets/worksheet/
docs/
scripts/smoke_check.py
examples/student-workspace/
  curriculum/
  knowledge-points/
  memory/
  mistakes/
  records/
  weak-points/
  worksheets/
```

## Use With OpenClaw

OpenClaw supports AgentSkills-style `SKILL.md` folders in workspace-level `skills/` directories and user-level skill directories. See the OpenClaw skills documentation: <https://docs.openclaw.ai/tools/skills>.

This project keeps the skill at:

```text
skills/zhizhi-math-coach
```

Typical use:

1. Create a separate personal learning repository for one child or family. The repository can be public or private; that choice belongs to the user.
2. Open that repository as the OpenClaw workspace.
3. Install `zhizhi-math-coach` from ClawHub into the workspace or user skills location.
4. Initialize the learning files with `skills/zhizhi-math-coach/scripts/init_learning_workspace.py`, or ask `$zhizhi-math-coach` to initialize the personal learning repository.
5. Replace the generated profile, curriculum, memory, knowledge-point, and weak-point placeholders with real local context.
6. Ask OpenClaw to use `$zhizhi-math-coach` while working inside the personal learning repository.

Example prompts:

```text
$zhizhi-math-coach 批改这几道错题，记录薄弱项并给家长讲解稿。
$zhizhi-math-coach 根据最近错题变式出一张 10 分钟练习卷。
$zhizhi-math-coach 针对退位减法薄弱项出专项练习，并给答案和复评标准。
$zhizhi-math-coach 生成一年级下册人教版当前范围的期末错因复习卷。
```

## Workspace And Skill Source Model

For normal ClawHub users, there is one Git repository: the personal learning repository. The installed skill may live inside that workspace, but it is just a downloaded capability bundle, not the data store.

```text
zhizhi-math-learning-data/         # personal learning repository, opened as the OpenClaw workspace
  .git/
  skills/zhizhi-math-coach/        # installed from ClawHub; usually not committed
  curriculum/
  knowledge-points/
  memory/
  mistakes/
  records/
  weak-points/
  worksheets/
  site/
```

For skill development, there may also be a separate source repository:

```text
zhizhi-math-coach-openclaw/        # reusable skill source repository
  skills/zhizhi-math-coach/        # SKILL.md, references, scripts, templates
  examples/student-workspace/      # starter template and sanitized examples
```

The skill source or installed skill provides the capability. The personal learning repository stores the data and generated outputs.

When OpenClaw runs `$zhizhi-math-coach`, the skill instructions may be loaded from `skills/zhizhi-math-coach`, but learning files are read from and written to the current OpenClaw workspace. In normal use, that workspace should be `zhizhi-math-learning-data/`.

Working directory rules:

- Daily grading, diagnosis, explanation, worksheet generation, worksheet publishing, and Git sync: work inside `zhizhi-math-learning-data/`.
- Skill development, template changes, sample generation, smoke checks, README updates, and ClawHub/GitHub release work: work inside `zhizhi-math-coach-openclaw/`.
- Do not switch to `zhizhi-math-coach-openclaw/` for a student's normal learning session.
- When in doubt, run `pwd` first. If the path ends in `zhizhi-math-coach-openclaw`, you are editing the reusable skill repository, not the student's learning archive.

Output locations:

- grading or diagnosis writes `records/`, `mistakes/`, `weak-points/`, and sometimes `memory/` in the personal repository;
- explanation cards write or update `knowledge-points/` in the personal repository;
- worksheet generation writes `worksheets/<date-topic>/worksheet-spec.json`, `worksheet.html`, and `answer-key.md` in the personal repository;
- publishing writes `site/` and `worksheets/<date-topic>/publish.json` in the personal repository.

Scripts can be executed from the installed skill path, and their input and workspace arguments should point to the personal repository. For example, run `skills/zhizhi-math-coach/scripts/publish_html_site.py` with `--workspace .` only when the shell is currently inside `zhizhi-math-learning-data/`.

Do not run regular student learning sessions with `zhizhi-math-coach-openclaw` as the workspace. If you do, generated learning data may be written into the reusable skill repository, which is only appropriate for development or sanitized examples.

## Generate A Sample Worksheet

From the repository root:

```bash
python3 skills/zhizhi-math-coach/scripts/generate_worksheet.py \
  examples/student-workspace/worksheets/sample-borrowing-subtraction/worksheet-spec.json
```

Outputs:

- `examples/student-workspace/worksheets/sample-borrowing-subtraction/worksheet.html`
- `examples/student-workspace/worksheets/sample-borrowing-subtraction/answer-key.md`

Validate a worksheet spec without writing output:

```bash
python3 skills/zhizhi-math-coach/scripts/validate_worksheet_spec.py \
  examples/student-workspace/worksheets/sample-borrowing-subtraction/worksheet-spec.json
```

Run the repository smoke check:

```bash
python3 scripts/smoke_check.py
```

If browser print verification is needed, add `--verify-print` to generation and make sure Chrome or Chromium is installed.

## Personal Learning Repository

This repository is the reusable skill. Real generated data belongs in a separate personal learning repository.

The personal learning repository can be public or private. If it is public, keep sensitive learning records out of `site/` and avoid committing sensitive raw inputs.

Recommended personal repository layout:

```text
zhizhi-math-learning-data/
  README.md
  .gitignore
  curriculum/
  knowledge-points/
  memory/
  mistakes/
  records/
  weak-points/
  worksheets/
  site/
```

Initialize a personal learning repository after installing the skill from ClawHub:

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

The generated `.gitignore` ignores `skills/` by default so downloaded ClawHub bundles are not committed into the personal learning repository. Reinstall the skill on another machine when needed.

## What Triggers Local Updates And Sync

There is no background sync by default.

Local learning files are updated when OpenClaw is working inside the personal learning repository and the user invokes the skill, for example:

```text
$zhizhi-math-coach 批改这张练习卷，记录薄弱项。
$zhizhi-math-coach 根据最近错题生成变式练习。
```

Typical write triggers:

- grading or diagnosis updates `records/`, `mistakes/`, `weak-points/`, and sometimes `memory/`;
- worksheet generation updates `worksheets/<date-topic>/worksheet-spec.json`, `worksheet.html`, and `answer-key.md`;
- publishing updates `site/` and `worksheets/<date-topic>/publish.json`;
- scheduled OpenClaw tasks only remind or suggest by default, unless the parent explicitly asks them to write records or generate worksheets.

GitHub sync happens only when the user commits and pushes from the personal learning repository. For a private personal repository, this can archive the full learning state:

```bash
git add curriculum knowledge-points memory mistakes records weak-points worksheets site
git commit -m "Update learning records"
git push
```

For a public personal repository, commit only files that are safe to expose. In most cases that means `site/` only, or sanitized worksheet files without answers or student identifiers.

## Publish Child-Facing HTML From The Personal Repository

When public worksheet links are acceptable, run the publisher in the personal learning repository. It publishes only child-facing HTML into that repository's `site/` directory:

```bash
python3 skills/zhizhi-math-coach/scripts/publish_html_site.py \
  worksheets \
  --workspace . \
  --base-url https://<user>.github.io/zhizhi-math-learning-data
```

The publisher writes:

- `site/index.html` in the personal repository: public worksheet list.
- `site/worksheets/<slug>/index.html`: printable child-facing worksheet page.
- `site/.nojekyll`: GitHub Pages static-site marker.
- `worksheets/<date-topic>/publish.json`: publication manifest.

Do not publish answer keys, grading records, memory files, weak-point history, uploaded papers, or textbook files to `site/`.

To publish on GitHub, enable Pages in the personal learning repository settings and choose the `site/` directory or a workflow copied from `docs/personal-learning-repo-template.md`.

## Supported Worksheet Strategies

- `wrong_question_variant`: create variants from known wrong questions.
- `weak_point_drill`: focus one weak point with targeted item mix.
- `exam_mistake_review`: midterm/final review weighted by this semester's mistakes.
- `relapse_repair`: handle relapse, transfer failure, or spaced forgetting.
- `spaced_review`: revisit old weak points on a 1/3/7/14-day rhythm.
- `transfer_check`: change wording, scenario, or condition order to verify transfer.
- `post_explanation_check`: short validation set after a parent explanation.
- `diagnostic_probe`: short set to separate reading, modeling, calculation, and checking causes.
- `mixed_maintenance`: keep current unit, old weak points, and fluency alive.
- `geometry_drill`: render deterministic SVG/HTML geometry items from structured specs.

When a parent only says "出一张练习卷", confirm purpose, content scope, length, and output format before generating.

For Feishu delivery, prefer sending the GitHub Pages worksheet URL when the page is public-safe. Keep `answer-key.md` outside the published `site/` directory.

## Curriculum Boundary

This skill can use textbook metadata and local curriculum files to avoid out-of-scope practice. For example, a personal workspace may point to an external source such as `TapXWorld/ChinaTextbook` for the 人教版小学数学目录, but this public repository must not commit textbook PDFs, screenshots, or copied textbook problem sets.

Use textbook information for:

- grade, semester, volume, unit, and knowledge-point alignment;
- midterm/final scope planning;
- parent explanation level and terminology;
- original diagnostic and variant problems.

Do not use it to duplicate copyrighted textbook content.

## Privacy Boundary

Do not commit:

- real student names or school names;
- completed worksheet images;
- school papers or teacher feedback screenshots;
- personal mistake books, records, memory files, curriculum progress, or knowledge-point notes;
- downloaded textbook PDFs, screenshots, scans, or OCR output.

Use this repository for reusable instructions, generators, templates, validators, and sanitized examples only.
