"""Regression and end-to-end checks; all mutations use temporary workspaces."""

from __future__ import annotations

import contextlib
import copy
import datetime as dt
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/zhizhi-math-coach/scripts"
sys.path.insert(0, str(SCRIPTS))

import build_grading_context as context
import generate_visual_practice as visual
import generate_worksheet as generator
import git_scope
import knowledge_assessment as knowledge
import model_worksheet
import photo_jobs
import publish_and_wait_pages as pages
import publish_html_site as publisher
import record_grading_diagnosis as recorder
import setup_scheduled_tasks as scheduled
import validate_diagnosis_payload as validator
import validate_worksheet_spec as worksheet_validator
import workspace_transaction as transaction
from geometry_primitives import render_extended_geometry, validate_geometry
from grading_followup import normalize_payload


MESSAGE = "Verify scoped recording\n\nAI-Co-Authored-By: Codex"


def payload() -> dict:
    items = []
    for index, result in enumerate(["correct", "wrong", "wrong", "need-confirmation"], 1):
        items.append({"item_no": str(index), "question": "数一数三角形的个数。", "student_answer": "2",
                      "correct_answer": "2" if result == "correct" else "3", "result": result,
                      "page": 1, "confidence": "high", "recognition_confidence": "high" if result != "need-confirmation" else "low",
                      "knowledge_points": [{"id": "geometry.shape-recognition", "title": "平面图形辨认与计数"}],
                      "cause": "重复计数", "error_type": "计算技能", "remediation": "每数一个图形做一个标记。"})
    return {"date": "2026-10-01", "source": "photo-test", "source_type": "school", "grade": "一年级",
            "semester": "上学期", "overall": "计数需要按顺序标记。", "items": items}


def main_json(module, argv: list[str]) -> dict:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = module.main(argv)
    if code:
        raise AssertionError(output.getvalue())
    return json.loads(output.getvalue())


class Workspaces(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / "learning"
        self.workspace.mkdir()

    def record(self, data=None, *args):
        path = Path(self.temp.name) / "payload.json"
        path.write_text(json.dumps(data or payload(), ensure_ascii=False), encoding="utf-8")
        return main_json(recorder, ["--workspace", str(self.workspace), "--input", str(path), "--no-log", *args])

    def test_full_paper_archive_and_knowledge(self):
        result = self.record()
        self.assertEqual(result["decision"]["mode"], "full_archive")
        self.assertEqual(result["decision"]["confirmation_items"], ["4"])
        diagnosis = next(p for p in result["written"] if p.endswith("diagnosis.md"))
        report = (self.workspace / diagnosis).read_text()
        self.assertIn("题 1 · 正确", report)
        self.assertIn("题 4 · 待确认", report)
        point = result["knowledge_assessment"][0]
        self.assertEqual(point["scored_items"], 3)
        self.assertEqual(point["status"], "需要巩固")
        self.assertTrue((self.workspace / "records/knowledge-mastery.md").exists())
        ctx = context.build_context(self.workspace)
        self.assertEqual(ctx["knowledge_assessment"][0]["id"], "geometry.shape-recognition")

    def test_retry_is_idempotent(self):
        first = self.record()
        before = {p: (self.workspace / p).read_bytes() for p in first["written"]}
        second = self.record()
        self.assertTrue(second["duplicate"])
        self.assertEqual(before, {p: (self.workspace / p).read_bytes() for p in before})

    def test_dry_run_is_read_only(self):
        self.record(None, "--dry-run")
        self.assertEqual(list(self.workspace.iterdir()), [])

    def test_explicit_id_rejects_changed_payload(self):
        data = payload()
        data["record_id"] = "batch-one"
        self.record(data)
        data["overall"] = "different"
        with self.assertRaisesRegex(ValueError, "different content"):
            self.record(data)

    def test_transaction_recovers_after_partial_write(self):
        original = transaction.atomic_write
        failed = False
        def interrupted(path, data):
            nonlocal failed
            if path.name == "school-mistakes.md" and not failed:
                failed = True
                raise OSError("simulated interruption")
            return original(path, data)
        with patch.object(transaction, "atomic_write", side_effect=interrupted):
            with self.assertRaises(OSError):
                self.record()
        self.assertTrue((self.workspace / ".zhizhi-math-coach/recording-pending.json").exists())
        result = self.record()
        self.assertTrue(result["duplicate"])
        self.assertEqual(len(list((self.workspace / "records").glob("*-diagnosis.md"))), 1)
        self.assertFalse((self.workspace / ".zhizhi-math-coach/recording-pending.json").exists())

    def test_path_traversal_and_invalid_counts_rejected(self):
        for field, value in [("date", "../../outside"), ("date", "2026-02-30"), ("correct_items", 8), ("total_items", -1)]:
            data = normalize_payload(payload())
            data[field] = value
            self.assertTrue(validator.validate_payload(data, mode="auto")[0])

    def test_symlink_output_rejected(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.workspace / "records").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.record()
        self.assertEqual(list(outside.iterdir()), [])

    def test_correct_paper_still_documented(self):
        data = payload()
        for item in data["items"]:
            item.update(result="correct", recognition_confidence="high")
        result = self.record(data)
        self.assertEqual(result["decision"]["mode"], "fast_grade_light_record")
        self.assertFalse((self.workspace / "mistakes/school-mistakes.md").exists())
        self.assertEqual(result["knowledge_assessment"][0]["status"], "初步掌握")

    def test_knowledge_needs_spaced_independent_evidence(self):
        data = normalize_payload(payload())
        for item in data["items"]:
            item.update(result="correct", recognition_confidence="high")
        first = knowledge.assess_knowledge({}, data, "records/first.md")
        key = "geometry.shape-recognition"
        self.assertEqual(first["concepts"][key]["status"], "初步掌握")
        data["date"] = "2026-10-08"
        second = knowledge.assess_knowledge(first, data, "records/second.md")
        self.assertEqual(second["concepts"][key]["status"], "稳定掌握")
        data["date"] = "2026-10-09"
        for item in data["items"]:
            item["assisted"] = True
        third = knowledge.assess_knowledge(second, data, "records/third.md")
        self.assertEqual(third["concepts"][key]["status"], "待确认")
        self.assertEqual(third["concepts"][key]["scored_items"], 8)

    def test_photo_queue_archives_images_and_rejects_other_workers(self):
        image = self.workspace / "input.png"
        image.write_bytes(b"test image bytes")
        prefix = ["--workspace", str(self.workspace)]
        queued = main_json(photo_jobs, [*prefix, "enqueue", "--image", str(image), "--date", "2026-10-01"])
        duplicate = main_json(photo_jobs, [*prefix, "enqueue", "--image", str(image), "--date", "2026-10-01"])
        self.assertTrue(duplicate["duplicate"])
        job = main_json(photo_jobs, [*prefix, "claim"])["job"]
        self.assertIsNone(main_json(photo_jobs, [*prefix, "claim"])["job"])
        with self.assertRaises(ValueError):
            main_json(photo_jobs, [*prefix, "fail", "--job-id", job["id"], "--lease-token", "other", "--error", "failure"])
        source = Path(self.temp.name) / "input.json"
        source.write_text(json.dumps(payload()))
        image.unlink()  # The queue owns a durable copy.
        finished = main_json(photo_jobs, [*prefix, "finish", "--job-id", job["id"], "--lease-token", job["lease_token"], "--input", str(source)])
        self.assertEqual(finished["status"], "needs-confirmation")
        self.assertEqual(queued["id"], finished["id"])
        images = [path for path in finished["result"]["written"] if path.endswith(".png")]
        self.assertEqual(len(images), 1)
        self.assertEqual((self.workspace / images[0]).read_bytes(), b"test image bytes")

    def test_multiconcept_wrong_answer_requires_step_evidence(self):
        data = payload()
        item = data["items"][1]
        item["knowledge_points"].append({"id": "number.counting", "title": "计数"})
        data["items"] = [item]
        state = knowledge.assess_knowledge({}, data, "records/first.md")
        self.assertTrue(all(point["scored_items"] == 0 for point in state["concepts"].values()))
        item["knowledge_points"][0]["result"] = "correct"
        item["knowledge_points"][1]["result"] = "wrong"
        state = knowledge.assess_knowledge({}, data, "records/second.md")
        self.assertEqual(state["concepts"]["geometry.shape-recognition"]["observed_accuracy"], 1)
        self.assertEqual(state["concepts"]["number.counting"]["status"], "需要巩固")

    def test_auto_visual_practice_uses_assessed_topic(self):
        self.record()
        path = Path(self.temp.name) / "visual.json"
        with patch.object(sys, "argv", ["visual", "--kind", "auto", "--workspace", str(self.workspace), "--output", str(path)]), contextlib.redirect_stdout(io.StringIO()):
            visual.main()
        spec = json.loads(path.read_text())
        self.assertEqual(spec["based_on_knowledge_point"], "geometry.shape-recognition")
        self.assertEqual(spec["sections"][0]["items"][0]["geometry_spec"]["type"], "shape_collection")

    def test_photo_timeout_reclaimed_and_retry_limit(self):
        image = self.workspace / "input.png"
        image.write_bytes(b"image")
        prefix = ["--workspace", str(self.workspace)]
        main_json(photo_jobs, [*prefix, "enqueue", "--image", str(image)])
        with patch.object(photo_jobs.time, "time", return_value=100):
            first = main_json(photo_jobs, [*prefix, "claim", "--lease-seconds", "30"])["job"]
        with patch.object(photo_jobs.time, "time", return_value=131):
            second = main_json(photo_jobs, [*prefix, "claim", "--lease-seconds", "30"])["job"]
        self.assertNotEqual(first["lease_token"], second["lease_token"])
        with patch.object(photo_jobs.time, "time", return_value=162):
            main_json(photo_jobs, [*prefix, "claim", "--lease-seconds", "30"])
        with patch.object(photo_jobs.time, "time", return_value=193):
            self.assertIsNone(main_json(photo_jobs, [*prefix, "claim"])["job"])
        self.assertEqual(main_json(photo_jobs, [*prefix, "list"])["jobs"][0]["status"], "failed")

    def test_publish_only_selected_and_keep_old_index(self):
        for name in ("one", "two", "draft"):
            directory = self.workspace / "worksheets" / name
            directory.mkdir(parents=True)
            (directory / "worksheet.html").write_text(f"<html>{name}</html>")
        for name in ("one", "two"):
            with patch.object(sys, "argv", ["publish_html_site.py", f"worksheets/{name}", "--workspace", str(self.workspace)]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(publisher.main(), 0)
        self.assertFalse((self.workspace / "site/worksheets/draft").exists())
        index = (self.workspace / "site/index.html").read_text()
        self.assertIn("worksheets/one/", index)
        self.assertIn("worksheets/two/", index)
        self.assertNotIn("worksheets/draft/", index)

    def test_scoped_git_commit_preserves_unrelated_index_and_deletions(self):
        def git(*args):
            return subprocess.check_output(["git", *args], cwd=self.workspace, text=True, stderr=subprocess.STDOUT)
        git("init", "-q")
        git("config", "user.name", "Temporary Test")
        git("config", "user.email", "test@example.invalid")
        (self.workspace / "site").mkdir()
        page = self.workspace / "site/index.html"
        page.write_text("one")
        private = self.workspace / "private.txt"
        private.write_text("private")
        git("add", "private.txt")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(git_scope.commit_scope(self.workspace, ["site"], MESSAGE))
        self.assertEqual(git("show", "--pretty=format:", "--name-only", "HEAD").strip(), "site/index.html")
        self.assertEqual(git("diff", "--cached", "--name-only").strip(), "private.txt")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(git_scope.commit_scope(self.workspace, ["site"], MESSAGE))
            page.unlink()
            self.assertTrue(git_scope.commit_scope(self.workspace, ["site"], MESSAGE))
        self.assertEqual(git("diff", "--cached", "--name-only").strip(), "private.txt")

    def test_scheduled_worker_is_explicit_and_configured(self):
        config = scheduled.ensure_automation_config(self.workspace, False, "Asia/Shanghai", True)
        self.assertTrue(config["automation"]["allow_photo_archive"])
        self.assertFalse(config["automation"]["allow_auto_worksheet_generation"])
        task = next(t for t in config["automation"]["tasks"] if t["kind"] == "photo_archive")
        self.assertEqual(task["cron"], "*/5 * * * *")
        command = scheduled.build_command("openclaw", self.workspace, task, "Asia/Shanghai", None, None)
        self.assertIn("claim", command[command.index("--message") + 1])


class GeometryAndPublishing(unittest.TestCase):
    def model_spec(self):
        return json.loads((ROOT / "examples/student-workspace/worksheets/sample-model-designed/worksheet-spec.json").read_text())

    def test_english_model_output_keeps_generated_answer_labels_in_english(self):
        spec = json.loads((ROOT / "examples/student-workspace/worksheets/sample-model-english/worksheet-spec.json").read_text())
        spec["grading"] = {"error_labels": [{"name": "grouping", "description": "Recheck equal groups."}],
                           "reassessment": ["Check a new example independently."], "next": ["Try another route."]}
        for language in ("en", "en-GB", None):
            current = copy.deepcopy(spec)
            if language is None:
                current.pop("language")  # Infer English from the student document.
            else:
                current["language"] = language
            worksheet_validator.validate_semantics(current)
            html, answers, count = generator.render_html(current, generator.DEFAULT_TEMPLATE)
            key = generator.render_answer_key(current, answers, count)
            self.assertIn('<html lang="en">', html)
            self.assertIn("Explanation: ", key)
            self.assertIn("## Grading notes", key)
            self.assertIn("## Reassessment", key)
            self.assertIn("## Next practice", key)
            self.assertFalse(any("\u4e00" <= char <= "\u9fff" for char in html + key))
            self.assertEqual(count, 2)
            for question in current["questions"]:
                self.assertNotIn(question["explanation"], html)
        chinese = self.model_spec()
        _, answers, count = generator.render_html(chinese, generator.DEFAULT_TEMPLATE)
        self.assertIn("## 答案", generator.render_answer_key(chinese, answers, count))
        self.assertIn("解析：", answers[0])

    def test_model_authored_layout_uses_shared_a4_profile(self):
        spec = self.model_spec()
        worksheet_validator.validate_semantics(spec)
        html, answers, count = generator.render_html(spec, generator.DEFAULT_TEMPLATE)
        self.assertEqual(count, 6)
        self.assertIn('id="zhizhi-print-profile"', html)
        self.assertIn("size: A4; margin: 12mm", html)
        self.assertIn("font-size: 14pt !important", html)
        self.assertIn("letter-spacing: 0.02em", html)
        self.assertEqual(len(answers), 6)
        for answer in spec["questions"]:
            self.assertNotIn(answer["explanation"], html)

    def test_model_html_blocks_active_and_remote_content(self):
        for content in ['<script>alert(1)</script>', '<img src="https://example.invalid/photo.png">',
                        '<svg onload="alert(1)"></svg>', '<style>body {background:u/**/rl(https://example.invalid/x)}</style>',
                        '<svg><rect fill="url(https://example.invalid/x)"/></svg>']:
            spec = self.model_spec()
            spec["student_html"] = spec["student_html"].replace("</body>", content + "</body>")
            with self.assertRaises(ValueError):
                model_worksheet.validate_model_spec(spec)

    def test_model_question_and_answer_ids_must_match(self):
        spec = self.model_spec()
        spec["questions"].pop()
        with self.assertRaisesRegex(ValueError, "exactly once"):
            model_worksheet.validate_model_spec(spec)

    def test_visual_templates_validate_and_keep_answers_out_of_html(self):
        for kind in visual.KINDS:
            for seed in range(10):
                spec = visual.make_spec(kind, 4, seed, "2026-10-01")
                worksheet_validator.validate_semantics(spec)
                html, answers, count = generator.render_html(spec, generator.DEFAULT_TEMPLATE)
                self.assertEqual(count, 4)
                self.assertIn("<svg", html)
                self.assertNotIn("answer_detail", html)
                for answer in answers:
                    self.assertNotIn(answer, html)
                bad = copy.deepcopy(spec)
                bad["sections"][0]["items"][0]["answer_detail"] = "错误答案，应该被拒绝"
                with self.assertRaises(ValueError):
                    worksheet_validator.validate_semantics(bad)

    def test_bad_diagrams_rejected(self):
        cases = [{"type": "clock", "hour": 3, "minute": 70},
                 {"type": "number_line", "start": 10, "end": 0},
                 {"type": "grid", "rows": 2, "cols": 2, "shaded_cells": [[2, 0]]},
                 {"type": "grid", "shaded_cells": [[0, 0], [0, 0]]},
                 {"type": "shape_collection", "shapes": [{"kind": "circle", "x": 310, "y": 20}]},
                 {"type": "polygon", "points": [[1, 2]]}]
        for case in cases:
            with self.assertRaises(ValueError):
                validate_geometry(case)

    def test_clock_hour_hand_moves_with_minutes(self):
        diagram = render_extended_geometry({"type": "clock", "hour": 3, "minute": 30, "canvas_width": 220, "canvas_height": 220})
        self.assertIn('stroke-width="4"', diagram)
        self.assertNotIn("3:30", diagram)

    def test_generator_enforces_review_before_writes(self):
        spec = visual.make_spec("clock", 1, 1, "2026-10-01")
        spec.pop("review_status")
        spec["sections"][0]["items"][0].pop("review_status")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "worksheet-spec.json"
            path.write_text(json.dumps(spec))
            result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "generate_worksheet.py"), str(path), "--no-pdf"], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((path.parent / "worksheet.html").exists())

    def test_pages_wait_uses_post_rebase_sha(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(sys, "argv", ["pages", "--workspace", tmp, "--no-pull"]))
            for name, value in [("load_config", None), ("infer_owner_repo", ("owner", "repo")),
                                ("configured_branch", "main"), ("run_publish", []), ("rel_paths", ["site"]),
                                ("commit_scope", True), ("head_sha", "rebased-sha"), ("wait_for_urls", None)]:
                stack.enter_context(patch.object(pages, name, return_value=value))
            rebase = stack.enter_context(patch.object(pages, "pull_rebase_autostash"))
            stack.enter_context(patch.object(pages, "git", side_effect=[subprocess.CompletedProcess([], 1, "", "non-fast-forward"), subprocess.CompletedProcess([], 0, "pushed", "")]))
            wait = stack.enter_context(patch.object(pages, "wait_for_action"))
            with contextlib.redirect_stdout(io.StringIO()):
                pages.main()
            rebase.assert_called_once()
            self.assertEqual(wait.call_args.args[4], "rebased-sha")


if __name__ == "__main__":
    unittest.main()
