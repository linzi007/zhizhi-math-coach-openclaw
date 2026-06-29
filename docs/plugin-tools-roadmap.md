# Plugin Tools Roadmap

## Why Plugin Tools Later

The v1 release is a Skill-first release. The next step is to wrap deterministic actions as OpenClaw plugin tools so the model does less free-form work for validation, rendering, and audits.

Keep the teaching, diagnosis, memory rules, and worksheet strategy in the Skill. A future Plugin should only own stable execution surfaces: validating JSON, rendering HTML, publishing Pages, sending notifications, and auditing privacy boundaries.

Plugin value:

- structured inputs instead of shell command construction;
- faster and more reliable execution for repeated actions;
- clearer permission and credential boundaries for GitHub/Lark integrations;
- machine-readable errors for OpenClaw to recover from.

## Candidate Tools

### `build_grading_context`

Current v1 surface: `scripts/build_grading_context.py`.

Input:

```json
{ "workspace_path": ".", "format": "json" }
```

Output:

```json
{
  "mode_default": "fast_grade_light_record",
  "files_read": ["memory/active-context.md", "curriculum/profile.md"],
  "warnings": [],
  "active_context": "...",
  "curriculum_profile": "..."
}
```

### `validate_diagnosis_payload`

Current v1 surface: `scripts/validate_diagnosis_payload.py`.

Input:

```json
{ "payload_path": "diagnosis-update.json", "mode": "fast_grade_light_record" }
```

Output:

```json
{ "ok": true, "errors": [], "warnings": [] }
```

### `validate_worksheet_spec`

Input:

```json
{ "spec_path": "worksheets/YYYY-MM-DD-topic/worksheet-spec.json" }
```

Output:

```json
{ "ok": true, "items": 8, "warnings": [] }
```

### `generate_worksheet`

Input:

```json
{
  "spec_path": "worksheets/YYYY-MM-DD-topic/worksheet-spec.json",
  "verify_print": false
}
```

Output:

```json
{
  "worksheet_path": "worksheets/YYYY-MM-DD-topic/worksheet.html",
  "pdf_path": "worksheets/YYYY-MM-DD-topic/worksheet.pdf",
  "answer_key_path": "worksheets/YYYY-MM-DD-topic/answer-key.md",
  "items": 8
}
```

### `publish_pages_and_wait`

Input:

```json
{
  "workspace_path": ".",
  "worksheet_path": "worksheets/YYYY-MM-DD-topic",
  "base_url": "https://user.github.io/repo",
  "wait": true
}
```

Output:

```json
{
  "ok": true,
  "index_url": "https://user.github.io/repo/",
  "worksheet_url": "https://user.github.io/repo/worksheets/YYYY-MM-DD-topic/",
  "actions_url": "https://github.com/user/repo/actions/runs/123"
}
```

### `record_grading_diagnosis`

Current v1 surface: `scripts/record_grading_diagnosis.py`.

Input:

```json
{
  "workspace_path": ".",
  "diagnosis_payload_path": "diagnosis-update.json"
}
```

Output:

```json
{
  "ok": true,
  "written": [
    "records/YYYY-MM-DD-source-diagnosis.md",
    "records/learning-progress.md",
    "mistakes/school-mistakes.md",
    "weak-points/topic.md"
  ]
}
```

The plugin version should keep the same boundary: it writes provided diagnosis data, but it does not grade images, infer causes, or upload/sync files.

### `append_run_log`

Current v1 surface: `scripts/run_log.py` used by local scripts.

Output destination:

```text
.zhizhi-math-coach/run-log.jsonl
```

The plugin version should emit structured duration and status events for context build, validation, recording, sync, publishing, and worksheet generation.

### `send_lark_message`

Input:

```json
{
  "recipient": "parent",
  "text": "练习卷已发布：...",
  "links": ["https://user.github.io/repo/"]
}
```

Output:

```json
{ "ok": true, "message_id": "..." }
```

### `audit_student_workspace`

Input:

```json
{ "workspace_path": "." }
```

Output:

```json
{
  "missing_files": [],
  "privacy_warnings": [],
  "stale_reviews": []
}
```

### `audit_public_repo_privacy`

Input:

```json
{ "workspace_path": ".", "public_mode": true }
```

Output:

```json
{
  "ok": true,
  "public_safe": true,
  "warnings": []
}
```

### `render_geometry_svg`

Input:

```json
{ "geometry_spec": { "type": "rectangle", "width_label": "8 cm", "height_label": "5 cm" } }
```

Output:

```json
{ "svg": "<svg ...>", "warnings": [] }
```

## Guardrails

- Tools should operate on explicit local paths only.
- Tools should not upload sensitive student files.
- Tools should never write learning records unless the caller explicitly asks.
- Tools should return structured warnings instead of silently fixing ambiguous math.
- Plugin tools should not replace `SKILL.md`; they should make the Skill's stable steps safer and faster.
