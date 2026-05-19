#!/usr/bin/env python3
"""Create the GitHub Actions workflow that deploys the public site/ folder."""

from __future__ import annotations

import argparse
from pathlib import Path


WORKFLOW = """name: Deploy GitHub Pages

on:
  push:
    branches: ["main"]
    paths:
      - "site/**"
      - ".github/workflows/pages.yml"
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "site"
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install .github/workflows/pages.yml for publishing site/ with GitHub Actions.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing workflow file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    target = workspace / ".github" / "workflows" / "pages.yml"

    if target.exists() and not args.force:
        print(f"skipped: {target} already exists; use --force to overwrite")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(WORKFLOW, encoding="utf-8")
    print(f"written: {target}")
    print("next: in GitHub repository Settings -> Pages -> Build and deployment -> Source, choose GitHub Actions")
    print("next: commit and push .github/workflows/pages.yml and site/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
