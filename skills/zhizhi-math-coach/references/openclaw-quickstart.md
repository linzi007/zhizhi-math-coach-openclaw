# OpenClaw Quickstart

## Purpose

Use this reference when onboarding a parent or when the first reply in a personal learning workspace needs setup guidance.

Keep the user-facing reply short. Prefer a checklist and the next command/action over long architecture explanations.

## First-Use Checklist

1. Confirm the current workspace is the personal learning repository, not `zhizhi-math-coach-openclaw`.
2. If the learning files are missing, initialize:

```bash
python3 {baseDir}/scripts/init_learning_workspace.py \
  --workspace . \
  --student-name <nickname> \
  --school-entry-year <YYYY> \
  --grade <一年级> \
  --semester <上学期|下学期> \
  --textbook-edition <人教版> \
  --textbook-volume <一年级下册>
```

3. Check GitHub sync only if the parent wants sync, public links, or automatic Pages publishing:

```bash
python3 {baseDir}/scripts/check_git_sync.py --workspace . --check-push
```

4. If sync is not ready, generate a repository deploy key and send only the public key:

```bash
python3 {baseDir}/scripts/prepare_github_deploy_key.py \
  --workspace . \
  --github-owner <user> \
  --repo <repo> \
  --configure-remote
```

5. If public Pages is desired, confirm GitHub Settings -> Pages -> Source is `GitHub Actions`, then ensure the workflow exists:

```bash
python3 {baseDir}/scripts/setup_github_pages_workflow.py --workspace .
```

## Quick Prompt Reference

Use these prompt shapes in examples and replies:

- `$zhizhi-math-coach 批改这张练习卷，记录薄弱项。`
- `$zhizhi-math-coach 根据最近错题生成变式练习。`
- `$zhizhi-math-coach 针对退位减法薄弱项出专项练习。`
- `$zhizhi-math-coach 生成期末错因复习卷，并发布学生版链接。`

## Publish-Ready Checklist

Automatic Pages publishing is allowed when all are true:

- `.github/workflows/pages.yml` exists.
- The GitHub repository Pages source is `GitHub Actions`.
- The repository deploy key has write access.
- `check_git_sync.py --check-push` succeeds.
- The parent accepts public visibility of committed files in a public repository.

When ready, publish and wait:

```bash
python3 {baseDir}/scripts/publish_and_wait_pages.py \
  worksheets/YYYY-MM-DD-topic \
  --workspace . \
  --base-url https://<github-user>.github.io/<repo>
```

Reply with:

- Pages index URL.
- Newly generated worksheet URL.
- Local `worksheet.html` and `answer-key.md` paths.
- Any caveat if Actions failed or timed out.

## Public Repository Ruleset

Recommended ruleset for direct OpenClaw publishing:

- Name: `main protect`.
- Status: `Active`.
- Bypass:
  - `Deploy keys`: `Always allow`.
  - `Repository admin`: `Always allow`.
- Target: `main`, or `Default` if default branch is `main`.
- Enable: `Restrict updates`, `Restrict deletions`, `Block force pushes`.
- Do not enable: required PRs, status checks, signed commits, or deployment gates.

This lets OpenClaw push through the deploy key while public viewers cannot edit `main`.
