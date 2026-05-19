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
  scripts/check_git_sync.py
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

## Recommended Model

Use a vision-capable frontier reasoning model. For OpenAI API setups, use `gpt-5.2` or a newer GPT-5.x frontier model when available; start with medium reasoning for daily use and raise reasoning for hard cases.

This is recommended because the skill often needs to:

- read worksheet photos, handwritten answers, teacher marks, and geometry diagrams;
- identify unclear handwriting or cropped photos and ask for confirmation instead of guessing;
- compare new mistakes with long-term `memory/`, `records/`, `mistakes/`, and `weak-points/`;
- create valid `worksheet-spec.json`, printable HTML, answer keys, and dated diagnosis records;
- reason through multi-step word problems, geometry, exam review plans, and transfer-failure patterns.

Avoid small text-only models for photo grading, geometry, complex word problems, or memory updates. They may be acceptable for simple reminders or formatting existing records.

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

The generated `.gitignore` ignores `skills/` by default so downloaded ClawHub bundles are not committed into the personal learning repository. Reinstall the skill on another machine when needed. If the first `git push` fails, the local learning workspace is still usable; configure GitHub authorization on the current machine and retry sync later.

## GitHub Authorization For Sync

OpenClaw may run on a machine that has no GitHub CLI and no saved GitHub credentials. Some OpenClaw providers may also have no safe GitHub token environment-variable setup. GitHub sync only needs plain `git`, a remote, and push authorization. GitHub CLI `gh` is optional.

Prefer a GitHub Deploy key. The expected interaction is: OpenClaw generates an SSH public key for the personal learning repository, sends that public key to the parent through Lark/Feishu or the OpenClaw reply, and the parent adds it in the target repository Settings -> Deploy keys with `Allow write access` enabled.

```bash
python3 skills/zhizhi-math-coach/scripts/prepare_github_deploy_key.py \
  --workspace . \
  --configure-remote
```

If the personal learning repository has no `origin` remote yet, pass the target repository explicitly:

```bash
python3 skills/zhizhi-math-coach/scripts/prepare_github_deploy_key.py \
  --workspace . \
  --github-owner <user> \
  --repo zhizhi-math-learning-data \
  --configure-remote
```

OpenClaw should send only the public key, never the private key. Suggested Lark/Feishu message:

```text
Please add this OpenClaw public key to the GitHub repository:
Location: Settings -> Deploy keys -> Add deploy key
Permission: enable Allow write access
After adding it, reply "added" and I will check again and continue publishing.
```

After the parent adds the key, run:

```bash
python3 skills/zhizhi-math-coach/scripts/check_git_sync.py --workspace . --check-push
```

On the first use inside a personal learning repository, if GitHub sync is not ready, the skill should briefly mention this Deploy key setup. Later, when the parent asks to publish a worksheet, send a link, push, or sync, a failed preflight should return the local file paths and repeat the Deploy key guidance instead of failing worksheet generation.

If Deploy keys or SSH are not available, create a fine-grained GitHub personal access token for the personal learning repository only:

- Create path: GitHub web -> profile photo -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens -> Generate new token.
- Repository access: select only `zhizhi-math-learning-data` or the user's personal learning repository.
- Normal sync permission: `Contents: Read and write`.
- Optional workflow setup permission: add `Workflows: Read and write` only if committing `.github/workflows/pages.yml`.
- Optional Pages API permission: add `Pages: Read and write` only if automation will configure Pages through the GitHub API. It is not needed when Pages is enabled manually in GitHub Settings.

For HTTPS token use:

```bash
git remote set-url origin https://github.com/<user>/zhizhi-math-learning-data.git
git push --dry-run origin HEAD
```

When Git prompts, enter the GitHub username and use the token as the password. Do not paste tokens into OpenClaw chat and do not store tokens in repository files or remote URLs.

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

GitHub sync happens only when the user explicitly asks to sync/push/publish or manually commits and pushes from the personal learning repository. Before OpenClaw commits or pushes, it should run:

```bash
python3 skills/zhizhi-math-coach/scripts/check_git_sync.py --workspace . --check-push
```

If the preflight fails, the generated local files remain valid and sync can be retried after SSH or token authorization is configured.

For a private personal repository, sync can archive the full learning state:

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

`site/index.html` scans all public-safe child-facing worksheets under `worksheets/`, sorts them by date descending, and shows date, practice status, title, topic, grade, item count, and completion summary. Practice status is inferred from `worksheets/status.md` when available; otherwise generated worksheets are shown as `未练习`.

Do not publish answer keys, grading records, memory files, weak-point history, uploaded papers, or textbook files to `site/`.

To publish on GitHub, enable Pages in the personal learning repository settings and choose the `site/` directory or a workflow copied from `docs/personal-learning-repo-template.md`.

If GitHub says private repositories require an upgrade for Pages, you can make the personal learning repository public for free Pages, but be explicit about the visibility boundary: every tracked file in a public repository is viewable, not only `site/`. Non-collaborators cannot push to a public repository by default, so public visibility does not let other people edit `main`. Keep collaborators empty unless they should be able to modify the repository, and protect `main` in Settings -> Branches or Rulesets at least by blocking force pushes and deletion. Do not enable required-pull-request rules if OpenClaw should push `site/` and workflow updates directly.

Recommended GitHub Pages setup:

1. Settings -> Pages -> Build and deployment -> Source: choose `GitHub Actions`.
2. Add `.github/workflows/pages.yml` to the personal learning repository.
3. If OpenClaw already has write access through the Deploy key, it can create, commit, and push the workflow:

```bash
python3 skills/zhizhi-math-coach/scripts/setup_github_pages_workflow.py --workspace .
git add .github/workflows/pages.yml site
git commit -m "Configure GitHub Pages publishing"
git push
```

Recommended ruleset:

- Ruleset name: `main protect`
- Enforcement status: `Active`
- Bypass list:
  - `Deploy keys`: `Always allow`
  - `Repository admin`: `Always allow`
- Target branches: `main`, or `Default` if the default branch is `main`
- Enable:
  - `Restrict updates`
  - `Restrict deletions`
  - `Block force pushes`
- Do not enable:
  - `Require a pull request before merging`
  - `Require status checks to pass`
  - `Require signed commits`
  - `Require deployments to succeed`

This keeps the public repository viewable but lets only the deploy key and repository admin update `main`. OpenClaw can still push directly, so publishing does not require manual PR merges.

Automatic publishing flow:

- After public Pages, `.github/workflows/pages.yml`, and a writable Deploy key are configured, the skill auto-publishes new generated worksheets.
- OpenClaw generates local `worksheet.html` and `answer-key.md`, refreshes `site/`, then commits and pushes public-safe files.
- After GitHub Actions completes, OpenClaw replies with the Pages index URL and the generated worksheet URL.
- If Actions fails or times out, local files remain valid and OpenClaw returns local paths plus Actions/auth setup guidance.

Manual equivalent:

```bash
python3 skills/zhizhi-math-coach/scripts/publish_and_wait_pages.py \
  worksheets/<date-topic> \
  --workspace . \
  --base-url https://<user>.github.io/zhizhi-math-learning-data
```

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
