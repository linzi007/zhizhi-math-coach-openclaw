#!/usr/bin/env python3
"""Repository smoke check for zhizhi-math-coach."""

from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "zhizhi-math-coach"
GENERATOR_PATH = SKILL_DIR / "scripts" / "generate_worksheet.py"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_worksheet_spec.py"
PUBLISHER_PATH = SKILL_DIR / "scripts" / "publish_html_site.py"
INIT_WORKSPACE_PATH = SKILL_DIR / "scripts" / "init_learning_workspace.py"
WORKSPACE_CONFIG_PATH = SKILL_DIR / "scripts" / "learning_workspace_config.py"
CONFIGURE_WORKSPACE_PATH = SKILL_DIR / "scripts" / "configure_learning_workspace.py"
GIT_SYNC_CHECK_PATH = SKILL_DIR / "scripts" / "check_git_sync.py"
SYNC_LEARNING_REPO_PATH = SKILL_DIR / "scripts" / "sync_learning_repo.py"
BUILD_GRADING_CONTEXT_PATH = SKILL_DIR / "scripts" / "build_grading_context.py"
VALIDATE_DIAGNOSIS_PAYLOAD_PATH = SKILL_DIR / "scripts" / "validate_diagnosis_payload.py"
RECORD_DIAGNOSIS_PATH = SKILL_DIR / "scripts" / "record_grading_diagnosis.py"
RUN_LOG_PATH = SKILL_DIR / "scripts" / "run_log.py"
SCHEDULED_TASKS_SETUP_PATH = SKILL_DIR / "scripts" / "setup_scheduled_tasks.py"
DEPLOY_KEY_PREP_PATH = SKILL_DIR / "scripts" / "prepare_github_deploy_key.py"
PAGES_WORKFLOW_SETUP_PATH = SKILL_DIR / "scripts" / "setup_github_pages_workflow.py"
PUBLISH_AND_WAIT_PATH = SKILL_DIR / "scripts" / "publish_and_wait_pages.py"
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
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 0:
        paths = [REPO_ROOT / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]
    else:
        paths = [path for path in REPO_ROOT.rglob("*") if ".git" not in path.parts]

    for path in paths:
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


def check_workspace_config_loads() -> None:
    load_module(WORKSPACE_CONFIG_PATH, "learning_workspace_config")


def check_configure_workspace_loads() -> None:
    load_module(CONFIGURE_WORKSPACE_PATH, "learning_workspace_configurer")


def check_git_sync_checker_loads() -> None:
    load_module(GIT_SYNC_CHECK_PATH, "git_sync_checker")


def check_sync_learning_repo_loads() -> None:
    load_module(SYNC_LEARNING_REPO_PATH, "learning_repo_syncer")


def write_smoke_workspace_files(workspace: Path) -> None:
    for rel_path in ["records", "mistakes", "weak-points", "memory", "curriculum", ".zhizhi-math-coach"]:
        (workspace / rel_path).mkdir(parents=True, exist_ok=True)
    (workspace / ".zhizhi-math-coach/config.json").write_text(
        json.dumps(
            {
                "workspace_role": "personal-learning-data",
                "git_sync": {
                    "enabled": True,
                    "auto_pull_before_task": False,
                    "auto_commit_after_task": True,
                    "auto_push_after_task": True,
                    "defer_push_after_grading": True,
                },
                "pages": {"enabled": False, "auto_publish_worksheets": False},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (workspace / "memory/active-context.md").write_text(
        "# Active Context\n\n- Updated: 2026-06-29\n- Smoke active context\n",
        encoding="utf-8",
    )
    (workspace / "curriculum/profile.md").write_text(
        "# Curriculum Profile\n\n- Grade: 一年级\n- Semester: 下学期\n",
        encoding="utf-8",
    )
    (workspace / "records/learning-progress.md").write_text(
        "# Learning Progress\n\n"
        "## Dated Records\n\n"
        "| Date | Type | Source/Topic | Result | Finding | Next Step |\n"
        "| --- | --- | --- | --- | --- | --- |\n",
        encoding="utf-8",
    )
    (workspace / "mistakes/school-mistakes.md").write_text(
        "# School Mistakes\n\n## Entries\n",
        encoding="utf-8",
    )


def smoke_payload() -> dict[str, object]:
    return {
        "date": "2026-06-29",
        "source_slug": "photo-smoke",
        "source": "photo smoke",
        "source_type": "school",
        "grade": "一年级",
        "semester": "一年级下学期",
        "total_items": 1,
        "correct_items": 0,
        "overall": "smoke diagnosis",
        "mistakes": [
            {
                "item_no": "1",
                "question": "1 + 1 = ?",
                "student_answer": "3",
                "correct_answer": "2",
                "result": "wrong",
                "error_type": "计算技能",
                "cause": "口算事实不熟",
                "weak_point_slug": "fact-fluency",
                "evidence": "smoke evidence",
                "confidence": "高",
                "remediation": "short fluency check",
            }
        ],
        "weak_points": [
            {
                "slug": "fact-fluency",
                "title": "口算事实",
                "status": "观察中",
                "history_note": "smoke evidence",
                "next_action": "short fluency check",
            }
        ],
        "progress": {
            "result": "0/1",
            "finding": "smoke diagnosis",
            "next_step": "short fluency check",
        },
        "active_context_md": "# Active Context\n\n- Updated: 2026-06-29\n- Smoke active context\n",
    }


def run_module_main(module, argv: list[str]) -> tuple[int, str]:
    old_argv = sys.argv[:]
    stdout = io.StringIO()
    try:
        sys.argv = argv
        with contextlib.redirect_stdout(stdout):
            result = module.main()
    finally:
        sys.argv = old_argv
    return result, stdout.getvalue()


def check_grading_context_payload_pipeline() -> None:
    load_module(RUN_LOG_PATH, "zhizhi_run_log")
    build_module = load_module(BUILD_GRADING_CONTEXT_PATH, "grading_context_builder")
    validate_module = load_module(VALIDATE_DIAGNOSIS_PAYLOAD_PATH, "diagnosis_payload_validator")
    record_module = load_module(RECORD_DIAGNOSIS_PATH, "grading_diagnosis_recorder_pipeline")
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "learning-data"
        write_smoke_workspace_files(workspace)
        payload = smoke_payload()
        payload_path = workspace / "payload.json"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

        result, stdout = run_module_main(
            build_module,
            [
                "build_grading_context.py",
                "--workspace",
                str(workspace),
                "--format",
                "json",
                "--run-id",
                "smoke",
            ],
        )
        if result != 0:
            fail("build_grading_context.py returned non-zero")
        context = json.loads(stdout)
        if context.get("mode_default") != "fast_grade_light_record":
            fail("build_grading_context.py did not set default grading mode")
        if "memory/active-context.md" not in context.get("files_read", []):
            fail("build_grading_context.py did not read active context")
        if context.get("warnings"):
            fail(f"build_grading_context.py emitted unexpected warnings: {context['warnings']}")

        result, stdout = run_module_main(
            validate_module,
            [
                "validate_diagnosis_payload.py",
                "--workspace",
                str(workspace),
                "--mode",
                "full_archive",
                "--input",
                str(payload_path),
                "--run-id",
                "smoke",
            ],
        )
        if result != 0:
            fail("validate_diagnosis_payload.py rejected valid payload")
        validation = json.loads(stdout)
        if not validation.get("ok"):
            fail("validate_diagnosis_payload.py did not report ok")

        invalid_path = workspace / "invalid.json"
        invalid_payload = dict(payload)
        invalid_payload.pop("source")
        invalid_path.write_text(json.dumps(invalid_payload, ensure_ascii=False), encoding="utf-8")
        result, stdout = run_module_main(
            validate_module,
            [
                "validate_diagnosis_payload.py",
                "--workspace",
                str(workspace),
                "--input",
                str(invalid_path),
                "--run-id",
                "smoke",
            ],
        )
        if result == 0:
            fail("validate_diagnosis_payload.py accepted invalid payload")
        invalid_validation = json.loads(stdout)
        if "missing top-level field: source" not in invalid_validation.get("errors", []):
            fail("validate_diagnosis_payload.py did not report missing source")

        result, stdout = run_module_main(
            record_module,
            [
                "record_grading_diagnosis.py",
                "--workspace",
                str(workspace),
                "--mode",
                "full_archive",
                "--input",
                str(payload_path),
                "--run-id",
                "smoke",
            ],
        )
        if result != 0:
            fail("record_grading_diagnosis.py returned non-zero")
        output = json.loads(stdout)
        if not output.get("ok"):
            fail("record_grading_diagnosis.py did not report ok")
        if not (workspace / "records/2026-06-29-photo-smoke-diagnosis.md").exists():
            fail("record_grading_diagnosis.py did not create diagnosis record")
        if "题1" not in (workspace / "mistakes/school-mistakes.md").read_text(encoding="utf-8"):
            fail("record_grading_diagnosis.py did not append mistake entry")
        if "photo smoke" not in (workspace / "records/learning-progress.md").read_text(encoding="utf-8"):
            fail("record_grading_diagnosis.py did not append progress row")
        if not (workspace / "weak-points/fact-fluency.md").exists():
            fail("record_grading_diagnosis.py did not create weak-point record")
        if "Smoke active context" not in (workspace / "memory/active-context.md").read_text(encoding="utf-8"):
            fail("record_grading_diagnosis.py did not refresh active context")
        progress_text = (workspace / "records/learning-progress.md").read_text(encoding="utf-8")
        if "\n\n| 2026-06-29 |" in progress_text:
            fail("record_grading_diagnosis.py inserted a blank line into the progress table")

        run_log_path = workspace / ".zhizhi-math-coach/run-log.jsonl"
        if not run_log_path.exists():
            fail("run-log.jsonl was not created")
        events = [json.loads(line) for line in run_log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        scripts = {event.get("script") for event in events}
        for script_name in ["build_grading_context.py", "validate_diagnosis_payload.py", "record_grading_diagnosis.py"]:
            if script_name not in scripts:
                fail(f"run-log.jsonl missing event for {script_name}")
        if not any(event.get("run_id") == "smoke" and event.get("ok") and event.get("duration_ms", -1) >= 0 for event in events):
            fail("run-log.jsonl missing successful smoke event with duration")


def check_record_grading_diagnosis_script() -> None:
    check_grading_context_payload_pipeline()


def check_scheduled_tasks_setup_loads() -> None:
    load_module(SCHEDULED_TASKS_SETUP_PATH, "scheduled_tasks_setup")


def check_deploy_key_preparer_loads() -> None:
    load_module(DEPLOY_KEY_PREP_PATH, "github_deploy_key_preparer")


def check_pages_workflow_setup_loads() -> None:
    load_module(PAGES_WORKFLOW_SETUP_PATH, "github_pages_workflow_setup")


def check_publish_and_wait_loads() -> None:
    load_module(PUBLISH_AND_WAIT_PATH, "github_pages_publish_and_wait")


def check_init_workspace_script() -> None:
    module = load_module(INIT_WORKSPACE_PATH, "learning_workspace_init")
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "learning-data"
        cmd_args = [
            "--workspace",
            str(target),
            "--student-name",
            "Smoke Test",
            "--school-entry-year",
            "2025",
            "--school-year",
            "2025-2026",
            "--grade",
            "一年级",
            "--semester",
            "下学期",
        ]
        old_argv = sys.argv[:]
        try:
            sys.argv = ["init_learning_workspace.py", *cmd_args]
            with contextlib.redirect_stdout(io.StringIO()):
                result = module.main()
        finally:
            sys.argv = old_argv
        if result != 0:
            fail("init_learning_workspace.py returned non-zero")

        required = [
            "README.md",
            ".zhizhi-math-coach/config.json",
            "memory/long-term.md",
            "memory/active-context.md",
            "memory/local-memory-rules.md",
            "curriculum/profile.md",
            "curriculum/school-calendar.md",
            "mistakes/index.md",
            "records/learning-progress.md",
            "weak-points/README.md",
            "worksheets/README.md",
            "site/README.md",
        ]
        for rel_path in required:
            if not (target / rel_path).exists():
                fail(f"init script did not create {rel_path}")

        long_term = (target / "memory/long-term.md").read_text(encoding="utf-8")
        if "Smoke Test" not in long_term or "一年级下学期" not in long_term:
            fail("init script did not apply student profile arguments")
        config = json.loads((target / ".zhizhi-math-coach/config.json").read_text(encoding="utf-8"))
        if config.get("workspace_role") != "personal-learning-data":
            fail("init script did not create personal-learning-data workspace config")
        if "automation" not in config:
            fail("init script did not create automation config section")


def main() -> int:
    check_skill_identity()
    check_no_public_binary_sources()
    check_worksheet_specs()
    check_site_public_boundary()
    check_publisher_loads()
    check_workspace_config_loads()
    check_configure_workspace_loads()
    check_git_sync_checker_loads()
    check_sync_learning_repo_loads()
    check_record_grading_diagnosis_script()
    check_scheduled_tasks_setup_loads()
    check_deploy_key_preparer_loads()
    check_pages_workflow_setup_loads()
    check_publish_and_wait_loads()
    check_init_workspace_script()
    print("ok: repository smoke check passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
