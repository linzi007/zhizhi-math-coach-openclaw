# GitHub Sync Authorization

## Purpose

OpenClaw may run on a machine that has no GitHub CLI, no SSH key, and no saved Git credentials. Do not assume GitHub sync is available.

The learning workflow must work in two layers:

1. Always generate local learning files first.
2. Sync to GitHub only after the parent asks for sync/publish and the current machine passes Git authorization checks.

## What Is Required

GitHub sync requires standard `git` access from the OpenClaw machine:

- `git` installed;
- the personal learning workspace is a Git repository;
- `origin` points to the target GitHub repository;
- current machine has push authorization through SSH key or HTTPS token.

GitHub CLI `gh` is optional. Do not require it.

ClawHub login is not GitHub repository authorization. Model provider login is not GitHub repository authorization.

## Recommended Authorization: SSH

Use SSH when possible because it does not require storing a token in commands.

Parent setup checklist:

```bash
git --version
ssh -T git@github.com
git remote -v
git remote set-url origin git@github.com:<user>/<repo>.git
git push --dry-run origin HEAD
```

If `ssh -T git@github.com` fails, the parent must add an SSH public key to GitHub on that machine/account.

## Alternative Authorization: HTTPS Token

Use HTTPS only when SSH is not available. The parent should create a fine-grained GitHub personal access token (PAT) scoped to the personal learning repository only.

Recommended token settings:

- Create path: GitHub web -> profile photo -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens -> Generate new token.
- Token type: fine-grained personal access token.
- Resource owner: the GitHub user or organization that owns the personal learning repository.
- Repository access: `Only select repositories`, then select only the personal learning repository, such as `zhizhi-math-learning-data`.
- Expiration: choose a finite expiry, for example 30 to 90 days, unless the parent has a managed secret-rotation process.
- Repository permissions for normal sync: `Contents: Read and write`.
- Repository permissions for optional workflow file setup: add `Workflows: Read and write` only if OpenClaw or local git will commit files under `.github/workflows/`.
- Repository permissions for GitHub Pages API management: add `Pages: Read and write` only if an automation will enable or update Pages through the GitHub API. This is not needed when the parent enables Pages in the GitHub web UI, and not needed for ordinary `git push` of `site/`.

Do not grant broad access such as `All repositories` or classic `repo` scope unless fine-grained tokens cannot satisfy the user's GitHub account or organization policy.

Do not ask the parent to paste tokens into chat. Do not write tokens into repository files.

Acceptable storage options depend on the machine:

- Git Credential Manager;
- OS keychain/credential helper;
- environment secret outside the repository;
- platform-managed secret store.

Parent setup checklist for HTTPS:

```bash
git --version
git remote -v
git remote set-url origin https://github.com/<user>/<repo>.git
git push --dry-run origin HEAD
```

When Git prompts for credentials, enter the GitHub username and use the PAT as the password. Never place the PAT in the remote URL, worksheet files, README files, prompts, or chat messages.

## Preflight

Before any automatic commit/push, run:

```bash
python3 {baseDir}/scripts/check_git_sync.py --workspace <personal-learning-workspace> --check-push
```

If the check fails, do not treat worksheet generation as failed. Return:

- local generated file paths;
- missing authorization item;
- exact command the parent can run to fix it;
- a note that sync can be retried later.

## Sync Policy

Do not run `git add`, `git commit`, or `git push` for ordinary generation. Sync only when the parent says "同步", "发布", "push", "提交到 GitHub", "发链接", or equivalent.

If sync is requested:

1. Generate or update local files.
2. If a child-facing link is requested, run `publish_html_site.py`.
3. Run the Git preflight.
4. If preflight passes, commit and push the requested scope.
5. If preflight fails, return local paths and setup guidance.

For public repositories, warn before committing `memory/`, `records/`, `mistakes/`, `weak-points/`, answer keys, uploads, or student identifiers.

For private repositories, full learning-state sync is acceptable after the parent asks for sync.

## GitHub Pages Note

GitHub Pages availability for private repositories depends on the user's GitHub plan. If Pages is not available or not authorized, keep local HTML output and Git sync separate: the worksheet still exists locally even if no public URL can be produced.
