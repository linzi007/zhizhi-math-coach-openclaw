#!/usr/bin/env python3
"""Check whether a workspace can sync to GitHub with plain git."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def line(status: str, message: str) -> None:
    print(f"{status}: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preflight check for GitHub sync from a personal learning workspace.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root. Defaults to current directory.")
    parser.add_argument("--remote", default="origin", help="Git remote name. Defaults to origin.")
    parser.add_argument("--check-push", action="store_true", help="Run git push --dry-run to test push authorization.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    ok = True

    if shutil.which("git") is None:
        line("missing", "git executable not found; OpenClaw can still generate local files, but cannot commit or push here")
        return 2

    if not workspace.exists():
        line("missing", f"workspace does not exist: {workspace}")
        return 2

    inside = run_git(["rev-parse", "--is-inside-work-tree"], workspace)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        line("missing", f"workspace is not a git repository: {workspace}")
        return 2
    line("ok", f"git repository detected: {workspace}")

    root = run_git(["rev-parse", "--show-toplevel"], workspace)
    if root.returncode == 0:
        line("ok", f"git root: {root.stdout.strip()}")

    remote = run_git(["remote", "get-url", args.remote], workspace)
    if remote.returncode != 0:
        line("missing", f"remote {args.remote!r} is not configured")
        ok = False
    else:
        line("ok", f"remote {args.remote}: {remote.stdout.strip()}")

    status = run_git(["status", "--short"], workspace)
    if status.returncode == 0:
        changed = [item for item in status.stdout.splitlines() if item.strip()]
        line("ok", f"working tree changes: {len(changed)}")

    if remote.returncode == 0:
        access = run_git(["ls-remote", args.remote], workspace)
        if access.returncode == 0:
            line("ok", f"remote {args.remote} is reachable with current git credentials")
        else:
            line("missing", f"remote {args.remote} is not reachable with current git credentials")
            if access.stderr.strip():
                line("detail", access.stderr.strip().splitlines()[-1])
            ok = False

    if ok and args.check_push:
        dry_run = run_git(["push", "--dry-run", args.remote, "HEAD"], workspace)
        if dry_run.returncode == 0:
            line("ok", "push dry-run succeeded")
        else:
            line("missing", "push dry-run failed")
            if dry_run.stderr.strip():
                line("detail", dry_run.stderr.strip().splitlines()[-1])
            ok = False

    if not ok:
        line("next", "generate local files only, then configure git/SSH/token on this machine or sync from another machine")
        return 1

    line("ready", "git sync can be attempted from this workspace")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
