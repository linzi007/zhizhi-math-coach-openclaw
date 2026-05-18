# Plugin Tools Roadmap

## Why Plugin Tools Later

The v1 release is a Skill-first release. The next step is to wrap deterministic actions as OpenClaw plugin tools so the model does less free-form work for validation, rendering, and audits.

## Candidate Tools

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
  "answer_key_path": "worksheets/YYYY-MM-DD-topic/answer-key.md",
  "items": 8
}
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
- Tools should not upload private student files.
- Tools should never write learning records unless the caller explicitly asks.
- Tools should return structured warnings instead of silently fixing ambiguous math.
