#!/usr/bin/env python3
"""Publish child-facing worksheet HTML files into a GitHub Pages site directory."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


FORBIDDEN_SITE_PARTS = {
    "answer-key.md",
    "records",
    "mistakes",
    "memory",
    "weak-points",
    "knowledge-points",
    "curriculum",
    "uploads",
    "textbooks",
    "ocr-output",
}
FORBIDDEN_HTML_MARKERS = {
    "answer_detail",
    "答案与批改标准",
    "## 答案",
    "批改重点",
    "复评标准",
}


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def rel_to(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def discover_worksheet_dirs(roots: list[Path]) -> list[Path]:
    dirs: set[Path] = set()
    for root in roots:
        if root.is_file() and root.name == "worksheet.html":
            dirs.add(root.parent)
        elif root.is_dir() and (root / "worksheet.html").exists():
            dirs.add(root)
        elif root.is_dir():
            for html_path in root.rglob("worksheet.html"):
                dirs.add(html_path.parent)
    return sorted(dirs)


def safe_slug(worksheet_dir: Path, workspace: Path) -> str:
    try:
        rel = worksheet_dir.resolve().relative_to(workspace.resolve())
        parts = [part for part in rel.parts if part not in {"worksheets", "examples", "student-workspace"}]
        if parts:
            return "-".join(parts)
    except ValueError:
        pass
    return worksheet_dir.name


def assert_public_html_safe(html_path: Path) -> None:
    text = html_path.read_text(encoding="utf-8")
    for marker in FORBIDDEN_HTML_MARKERS:
        if marker in text:
            raise ValueError(f"{html_path} contains forbidden public marker: {marker}")


def assert_site_safe(site_dir: Path) -> None:
    if not site_dir.exists():
        return
    for path in site_dir.rglob("*"):
        parts = set(path.parts)
        if parts & FORBIDDEN_SITE_PARTS:
            raise ValueError(f"forbidden path in public site: {path}")
        if path.name == "answer-key.md":
            raise ValueError(f"answer key must not be published: {path}")
        if path.is_file() and path.suffix.lower() == ".html":
            assert_public_html_safe(path)


def page_url(base_url: str | None, slug: str) -> str | None:
    if not base_url:
        return None
    return base_url.rstrip("/") + f"/worksheets/{slug}/"


def write_index(site_dir: Path, entries: list[dict]) -> None:
    items = []
    for entry in sorted(entries, key=lambda item: (item.get("date", ""), item.get("title", "")), reverse=True):
        title = e(entry.get("title") or entry["slug"])
        date = e(entry.get("date") or "")
        topic = e(entry.get("topic") or "")
        strategy = e(entry.get("strategy") or "")
        href = e(f"worksheets/{entry['slug']}/")
        meta = " / ".join(part for part in [date, topic, strategy] if part)
        items.append(
            "      <li>"
            f'<a href="{href}">{title}</a>'
            + (f'<span class="meta">{e(meta)}</span>' if meta else "")
            + "</li>"
        )

    html_text = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Zhizhi Math Coach Worksheets</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #111; background: #f7f7f7; }}
    main {{ max-width: 860px; margin: 0 auto; padding: 32px 18px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    p {{ margin: 0 0 20px; color: #555; }}
    ul {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }}
    li {{ background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 14px 16px; }}
    a {{ color: #0645d8; font-weight: 650; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .meta {{ display: block; margin-top: 6px; font-size: 14px; color: #666; }}
  </style>
</head>
<body>
  <main>
    <h1>Zhizhi Math Coach 练习卷</h1>
    <p>这里只发布学生可见练习卷；答案、批改记录和学习档案不进入公开站点。</p>
    <ul>
{chr(10).join(items) if items else "      <li>暂无练习卷</li>"}
    </ul>
  </main>
</body>
</html>
"""
    (site_dir / "index.html").write_text(html_text, encoding="utf-8")


def publish_one(worksheet_dir: Path, workspace: Path, site_dir: Path, base_url: str | None) -> dict:
    html_path = worksheet_dir / "worksheet.html"
    if not html_path.exists():
        raise ValueError(f"missing worksheet.html in {worksheet_dir}")
    assert_public_html_safe(html_path)

    spec_path = worksheet_dir / "worksheet-spec.json"
    spec = load_json(spec_path) if spec_path.exists() else {}
    slug = safe_slug(worksheet_dir, workspace)
    target_dir = site_dir / "worksheets" / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(html_path, target_dir / "index.html")

    url = page_url(base_url, slug)
    published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest = {
        "title": spec.get("title") or slug,
        "date": spec.get("date", ""),
        "topic": spec.get("topic", ""),
        "strategy": spec.get("strategy", ""),
        "source_worksheet": rel_to(html_path, workspace),
        "source_spec": rel_to(spec_path, workspace) if spec_path.exists() else "",
        "site_path": rel_to(target_dir / "index.html", workspace),
        "url": url,
        "visibility": "public-child-facing",
        "published_at": published_at,
    }
    (worksheet_dir / "publish.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"slug": slug, **manifest}


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish child-facing worksheet HTML files to a static site directory.")
    parser.add_argument("paths", nargs="*", type=Path, help="Worksheet directories, worksheet.html files, or roots to scan.")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Learning workspace root. Defaults to cwd.")
    parser.add_argument("--site-dir", type=Path, default=Path("site"), help="Output site directory relative to workspace.")
    parser.add_argument("--base-url", help="Optional GitHub Pages base URL, such as https://user.github.io/repo")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    site_dir = args.site_dir if args.site_dir.is_absolute() else workspace / args.site_dir
    roots = args.paths or [workspace / "worksheets", workspace / "examples" / "student-workspace" / "worksheets"]
    roots = [path if path.is_absolute() else workspace / path for path in roots]
    worksheet_dirs = discover_worksheet_dirs(roots)
    if not worksheet_dirs:
        raise ValueError("no worksheet.html files found")

    site_dir.mkdir(parents=True, exist_ok=True)
    (site_dir / ".nojekyll").write_text("", encoding="utf-8")
    entries = [publish_one(path, workspace, site_dir, args.base_url) for path in worksheet_dirs]
    write_index(site_dir, entries)
    assert_site_safe(site_dir)

    print(f"published: {site_dir}")
    for entry in entries:
        location = entry.get("url") or entry["site_path"]
        print(f"- {entry['title']}: {location}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
