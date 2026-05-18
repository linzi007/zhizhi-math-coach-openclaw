# Zhizhi Math Coach OpenClaw Skill

`zhizhi-math-coach` 是一个面向小学数学学习闭环的 OpenClaw Skill。它不是单次出题器，而是围绕真实练习证据持续跟进学习进度：

- 批改练习卷、学校作业、拍照图片或家长整理的错题；
- 判断错误类型、可能原因、关联知识点、薄弱项和复发/迁移失败情况；
- 维护短期记忆、长期记忆、学习进度、错题本和薄弱项记录；
- 结合中国年级、上下学期、期中期末、寒暑假、教材版本和实际教学进度规划练习；
- 生成家长讲解稿、学生简版说明、做题技巧和掌握标准；
- 根据错题、薄弱项或考前复习需求生成可打印 HTML 练习卷；
- 保持学生版练习卷无答案，家长版答案和批改标准单独保存。

本仓库只包含通用模板、脚本和脱敏示例。真实学生记录、试卷照片、学校作业、教材 PDF 和私有学习数据应放在单独的私有学习工作区。

## 项目结构

```text
skills/zhizhi-math-coach/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/generate_worksheet.py
  scripts/validate_worksheet_spec.py
  scripts/publish_html_site.py
  assets/worksheet/
.github/workflows/pages.yml
docs/
scripts/smoke_check.py
site/
examples/student-workspace/
  curriculum/
  knowledge-points/
  memory/
  mistakes/
  records/
  weak-points/
  worksheets/
```

## 在 OpenClaw 中使用

OpenClaw 支持 workspace 级别的 `skills/` 目录。当前 skill 路径为：

```text
skills/zhizhi-math-coach
```

典型使用方式：

1. 将本仓库作为 OpenClaw workspace 打开，或将 `skills/zhizhi-math-coach` 复制到你的 workspace/user skills 目录。
2. 将 `examples/student-workspace` 复制到私有学习项目中。
3. 替换示例中的学生信息、教材进度、记忆、知识点卡片和薄弱项记录。
4. 在 OpenClaw 中使用 `$zhizhi-math-coach` 触发批改、讲解、学习跟进或出卷。

示例：

```text
$zhizhi-math-coach 批改这几道错题，记录薄弱项并给家长讲解稿。
$zhizhi-math-coach 根据最近错题变式出一张 10 分钟练习卷。
$zhizhi-math-coach 针对退位减法薄弱项出专项练习，并给答案和复评标准。
$zhizhi-math-coach 生成一年级下册人教版当前范围的期末错因复习卷。
```

## 学习工作区

建议在私有学习项目中使用以下结构：

```text
curriculum/
  profile.md
  scope.md
  progress.md
  school-calendar.md
knowledge-points/
memory/
mistakes/
records/
weak-points/
worksheets/
```

核心文件用途：

- `memory/long-term.md`：稳定偏好、年级规则、教材版本、家长要求。
- `memory/short-term.md`：近期观察、当前优先级、待确认事项。
- `curriculum/profile.md`：学生年级、教材版本、册别、来源链接。
- `curriculum/school-calendar.md`：中国学年、上下学期、期中期末、寒暑假配置。
- `curriculum/progress.md`：学校当前教学进度、已学/未学范围。
- `knowledge-points/<topic>.md`：知识点讲解卡片。
- `weak-points/<topic>.md`：长期薄弱项记录。
- `mistakes/`：学校错题和系统练习错题。
- `records/learning-progress.md`：学习进度总览。
- `worksheets/`：练习卷 spec、HTML 和答案。

## 出卷方式

当前支持的出卷策略包括：

- `wrong_question_variant`：根据已有错题做变式训练。
- `weak_point_drill`：针对一个薄弱项做专项练习。
- `exam_mistake_review`：期中/期末按本学期错因和薄弱项复习。
- `relapse_repair`：处理复发、迁移失败或间隔遗忘。
- `spaced_review`：按间隔复习节奏回顾旧薄弱项。
- `transfer_check`：改变问法、场景或条件顺序，验证是否真正掌握。
- `post_explanation_check`：讲解后生成 3 到 6 道验证题。
- `diagnostic_probe`：短题组区分读题、建模、计算、检查等原因。
- `mixed_maintenance`：当前单元、旧薄弱项和计算熟练度混合保持。
- `geometry_drill`：使用结构化 `geometry_spec` 渲染 SVG/HTML 图形题。

当家长只说“出一张练习卷”时，skill 会先确认出卷目的、内容范围、题量/时长和输出形式。

## 生成示例练习卷

从仓库根目录运行：

```bash
python3 skills/zhizhi-math-coach/scripts/generate_worksheet.py \
  examples/student-workspace/worksheets/sample-borrowing-subtraction/worksheet-spec.json
```

输出：

- `examples/student-workspace/worksheets/sample-borrowing-subtraction/worksheet.html`
- `examples/student-workspace/worksheets/sample-borrowing-subtraction/answer-key.md`

只校验 spec、不写输出：

```bash
python3 skills/zhizhi-math-coach/scripts/validate_worksheet_spec.py \
  examples/student-workspace/worksheets/sample-borrowing-subtraction/worksheet-spec.json
```

运行仓库 smoke check：

```bash
python3 scripts/smoke_check.py
```

如果需要校验打印页数，可在生成命令中添加 `--verify-print`，并确保本机安装 Chrome 或 Chromium。

## 发布学生版 HTML 到 GitHub Pages

如果你接受练习卷公开访问，可以只把学生版 HTML 发布到 `site/`：

```bash
python3 skills/zhizhi-math-coach/scripts/publish_html_site.py \
  examples/student-workspace/worksheets \
  --base-url https://linzi007.github.io/zhizhi-math-coach-openclaw
```

脚本会生成：

- `site/index.html`：公开练习卷列表。
- `site/worksheets/<slug>/index.html`：可查看和打印的学生版练习卷。
- `site/.nojekyll`：GitHub Pages 静态站点标记。
- `worksheets/<date-topic>/publish.json`：在私有学习工作区运行时记录发布信息。

`site/` 只放学生可见内容。不要把答案、批改记录、长短期记忆、薄弱项历史、上传试卷、教材 PDF 或 OCR 内容放进去。

飞书里建议发送 GitHub Pages 链接，答案和批改标准仍保存在私有仓库。

要在线访问这些页面，需要在 GitHub 仓库 Settings -> Pages 中启用 Pages，并选择 **GitHub Actions** 作为部署来源。本仓库自带的 workflow 会发布已提交的 `site/` 目录。

## 教材使用边界

本项目可以使用教材信息帮助判断年级、册别、单元范围和知识点顺序。例如，私有学习工作区可以引用 `TapXWorld/ChinaTextbook` 中的人教版小学数学目录作为外部参考。

允许使用教材信息来做：

- 年级、学期、册别和单元范围对齐；
- 期中/期末复习范围规划；
- 家长讲解的语言层级控制；
- 原创诊断题、变式题和专项练习题生成。

不要将教材 PDF、教材截图、扫描件、OCR 内容或成套教材原题提交到公开仓库。

## OpenClaw 自动化建议

定时任务默认只做提醒和建议，不自动修改学生档案，也不自动出卷：

- 每日 20:30：提醒到期复练、待上传批改、短期记忆中待确认事项。
- 每周日 20:00：生成周复盘和下周建议。
- 学期结束后：生成学期总结和寒暑假复习池。
- 寒暑假期间：每周给出假期复习建议。

真正写入学习记录、改变薄弱项状态或生成新卷，应由家长确认或明确指令触发。

## 隐私边界

不要提交以下内容：

- 真实学生姓名或学校名称；
- 已完成练习卷图片；
- 学校试卷、作业或老师批改截图；
- 私有错题本、学习记录、记忆文件、教材进度或知识点笔记；
- 下载的教材 PDF、截图、扫描件或 OCR 输出。

本仓库用于复用 instruction、模板、脚本、校验器和脱敏示例。

## 发布说明

GitHub 发布和 ClawHub 收录是两件事：

- GitHub 用于公开源码、文档和示例。
- ClawHub 发布的是 `skills/zhizhi-math-coach` 这个 skill bundle。

发布前建议运行：

```bash
python3 scripts/smoke_check.py
```

更多发布说明见：

- `docs/openclaw-release.md`
- `docs/privacy-and-copyright.md`
- `docs/plugin-tools-roadmap.md`
