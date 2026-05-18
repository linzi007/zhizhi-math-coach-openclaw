# Sample Student Workspace

This folder is a sanitized example of a private learning workspace.

Copy it elsewhere before using it with a real child, then replace all sample data. Do not commit real student records back into this repository.

Suggested private layout:

```text
curriculum/
knowledge-points/
memory/
mistakes/
records/
weak-points/
worksheets/
```

Use the bundled generator from the repository root:

```bash
python3 skills/zhizhi-math-coach/scripts/generate_worksheet.py \
  examples/student-workspace/worksheets/sample-borrowing-subtraction/worksheet-spec.json
```

After copying this sample to a private workspace, replace all example profile, curriculum, memory, and weak-point data before using it with a real child.
