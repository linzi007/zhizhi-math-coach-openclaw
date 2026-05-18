#!/usr/bin/env python3
"""Repository smoke check for zhizhi-math-coach."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "zhizhi-math-coach"
GENERATOR_PATH = SKILL_DIR / "scripts" / "generate_worksheet.py"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_worksheet_spec.py"
PUBLISHER_PATH = SKILL_DIR / "scripts" / "publish_html_site.py"
FORBIDDEN_PUBLIC_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".heic"}
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
FORBIDDEN_SITE_MARKERS = {
    "answer_detail",
    "答案与批改标准",
    "## 答案",
    "批改重点",
    "复评标准",
}


def fail(message: str) -> None:
    raise RuntimeError(message)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_skill_identity() -> None:
    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.exists():
        fail("missing skills/zhizhi-math-coach/SKILL.md")
    text = skill_md.read_text(encoding="utf-8")
    if "name: zhizhi-math-coach" not in text:
        fail("SKILL.md frontmatter name must be zhizhi-math-coach")
    old_entrypoint = "$" + "math" + "-learning" + "-coach"
    if old_entrypoint in (REPO_ROOT / "README.md").read_text(encoding="utf-8"):
        fail("README still references the old skill entrypoint")


def check_no_public_binary_sources() -> None:
    for path in REPO_ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in FORBIDDEN_PUBLIC_EXTENSIONS:
            fail(f"forbidden public binary/source file: {path.relative_to(REPO_ROOT)}")


def copy_spec_to_temp(spec_path: Path, temp_root: Path) -> Path:
    rel = spec_path.relative_to(REPO_ROOT)
    target = temp_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(spec_path, target)
    return target


def check_worksheet_specs() -> None:
    generator = load_module(GENERATOR_PATH, "worksheet_generator")
    validator = load_module(VALIDATOR_PATH, "worksheet_validator")
    registry = generator.load_json(generator.TYPE_REGISTRY)
    specs = sorted(REPO_ROOT.glob("examples/**/worksheet-spec.json"))
    if not specs:
        fail("no worksheet-spec.json examples found")

    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        for spec_path in specs:
            spec = generator.load_json(spec_path)
            generator.validate_spec(spec, registry)
            validator.validate_semantics(spec)

            temp_spec = copy_spec_to_temp(spec_path, temp_root)
            temp_data = json.loads(temp_spec.read_text(encoding="utf-8"))
            html_text, answers, count = generator.render_html(temp_data, generator.DEFAULT_TEMPLATE)
            answer_key = generator.render_answer_key(temp_data, answers, count)
            if not html_text.strip() or not answer_key.strip():
                fail(f"empty render output for {spec_path}")
            if "answer_detail" in html_text:
                fail(f"child-facing worksheet leaked answer_detail field for {spec_path}")


def check_site_public_boundary() -> None:
    site_dir = REPO_ROOT / "site"
    if not site_dir.exists():
        return
    for path in site_dir.rglob("*"):
        if set(path.parts) & FORBIDDEN_SITE_PARTS:
            fail(f"forbidden path in public site: {path.relative_to(REPO_ROOT)}")
        if path.is_file() and path.suffix.lower() == ".html":
            text = path.read_text(encoding="utf-8")
            for marker in FORBIDDEN_SITE_MARKERS:
                if marker in text:
                    fail(f"public site html contains forbidden marker {marker!r}: {path.relative_to(REPO_ROOT)}")


def check_publisher_loads() -> None:
    load_module(PUBLISHER_PATH, "worksheet_publisher")


def main() -> int:
    check_skill_identity()
    check_no_public_binary_sources()
    check_worksheet_specs()
    check_site_public_boundary()
    check_publisher_loads()
    print("ok: repository smoke check passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
