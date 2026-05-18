# Long-Term Memory

## Student

- Display name: 示例学生
- Current stage: primary-school math.
- Education system: 中国大陆小学
- School entry year: 2025
- Current grade baseline on 2026-05-18: 一年级下学期
- Textbook: 人教版数学一年级下册
- Semester rule:
  - September 1 to January 31: first semester.
  - February 1 to August 31: second semester.

## Stable Preferences

- Parent-facing output should be concise Chinese.
- Child-facing worksheets should not include answers.
- Answers and grading rules stay in `answer-key.md`.
- Worksheets are printable HTML generated from `worksheet-spec.json`.
- Practice should target the cause of mistakes, not only repeat the same surface topic.
- Parent explanations should include a short script and quick verification questions.

## Stable Learning Rules

- Separate reading/modeling mistakes from calculation mistakes.
- Track school mistakes and generated-worksheet mistakes separately.
- Repaired weak points need spaced review before they are marked mastered.
- Do not generate out-of-scope content unless the parent explicitly asks for preview.
