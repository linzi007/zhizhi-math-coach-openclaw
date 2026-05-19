# Zhizhi Math Coach OpenClaw Skill

`zhizhi-math-coach` 是一个面向小学数学学习闭环的 OpenClaw Skill。它不是单次出题器，而是围绕真实练习证据持续跟进学习进度：

- 批改练习卷、学校作业、拍照图片或家长整理的错题；
- 判断错误类型、可能原因、关联知识点、薄弱项和复发/迁移失败情况；
- 维护短期记忆、长期记忆、学习进度、错题本和薄弱项记录；
- 结合中国年级、上下学期、期中期末、寒暑假、教材版本和实际教学进度规划练习；
- 生成家长讲解稿、学生简版说明、做题技巧和掌握标准；
- 根据错题、薄弱项或考前复习需求生成可打印 HTML 练习卷；
- 保持学生版练习卷无答案，家长版答案和批改标准单独保存。

本仓库只包含通用模板、脚本和脱敏示例。真实学生记录、试卷照片、学校作业、教材 PDF 和学习过程中生成的数据应放在单独的个人学习仓库。

## 项目结构

```text
skills/zhizhi-math-coach/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/init_learning_workspace.py
  scripts/generate_worksheet.py
  scripts/validate_worksheet_spec.py
  scripts/publish_html_site.py
  scripts/check_git_sync.py
  assets/worksheet/
docs/
scripts/smoke_check.py
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

1. 为一个孩子或家庭创建单独的个人学习仓库。这个仓库可以是 public，也可以是 private，由用户自己决定。
2. 将这个仓库作为 OpenClaw workspace 打开。
3. 从 ClawHub 将 `zhizhi-math-coach` 安装到 workspace 或 user skills 位置。
4. 使用 `skills/zhizhi-math-coach/scripts/init_learning_workspace.py` 初始化学习文件，或者直接让 `$zhizhi-math-coach` 初始化个人学习仓库。
5. 替换生成的学生信息、教材进度、记忆、知识点卡片和薄弱项占位内容。
6. 在个人学习仓库中使用 `$zhizhi-math-coach` 触发批改、讲解、学习跟进或出卷。

示例：

```text
$zhizhi-math-coach 批改这几道错题，记录薄弱项并给家长讲解稿。
$zhizhi-math-coach 根据最近错题变式出一张 10 分钟练习卷。
$zhizhi-math-coach 针对退位减法薄弱项出专项练习，并给答案和复评标准。
$zhizhi-math-coach 生成一年级下册人教版当前范围的期末错因复习卷。
```

## Workspace 和 Skill 来源如何协作

普通 ClawHub 用户通常只有一个 Git 仓库：个人学习仓库。安装下来的 skill 可以放在这个 workspace 里，但它只是能力包，不是数据仓库。

```text
zhizhi-math-learning-data/         # 个人学习仓库，作为 OpenClaw workspace 打开
  .git/
  skills/zhizhi-math-coach/        # 从 ClawHub 安装，通常不提交
  curriculum/
  knowledge-points/
  memory/
  mistakes/
  records/
  weak-points/
  worksheets/
  site/
```

如果是维护 skill 的开发者，才需要另一个源码仓库：

```text
zhizhi-math-coach-openclaw/        # 通用 skill 源码仓库
  skills/zhizhi-math-coach/        # SKILL.md、references、scripts、templates
  examples/student-workspace/      # 初始化模板和脱敏示例
```

skill 源码仓库或已安装的 skill 提供能力，`zhizhi-math-learning-data` 保存真实学习数据和生成结果。

OpenClaw 运行 `$zhizhi-math-coach` 时，会从 `skills/zhizhi-math-coach` 加载 skill 指令，但学习文件会从当前 OpenClaw workspace 读取，并写回当前 workspace。正常使用时，这个 workspace 应该是 `zhizhi-math-learning-data/`。

工作目录规则：

- 日常批改、诊断、讲解、出卷、发布学生版页面、同步个人学习数据：在 `zhizhi-math-learning-data/` 中工作。
- 修改 skill、更新模板、生成脱敏示例、运行 smoke check、改 README、准备 GitHub/ClawHub 发布：切到 `zhizhi-math-coach-openclaw/`。
- 不要在学生日常学习会话中把 `zhizhi-math-coach-openclaw/` 当 workspace 使用。
- 不确定当前目录时，先看 `pwd`。如果路径结尾是 `zhizhi-math-coach-openclaw`，说明你在维护通用 skill，不是在维护学生学习档案。

输出位置：

- 批改或诊断会写入个人仓库的 `records/`、`mistakes/`、`weak-points/`，必要时更新 `memory/`；
- 知识点讲解会写入或更新个人仓库的 `knowledge-points/`；
- 出卷会写入个人仓库的 `worksheets/<date-topic>/worksheet-spec.json`、`worksheet.html` 和 `answer-key.md`；
- 发布学生版页面会写入个人仓库的 `site/` 和 `worksheets/<date-topic>/publish.json`。

脚本可以从已安装的 skill 路径调用，但输入和 workspace 参数要指向个人学习仓库。例如在 `zhizhi-math-learning-data/` 目录中运行 `skills/zhizhi-math-coach/scripts/publish_html_site.py` 时，`--workspace .` 才表示发布到个人学习仓库。

## 推荐模型和原因

建议使用支持图片理解的前沿推理模型。如果使用 OpenAI API，建议使用 `gpt-5.2` 或更新的 GPT-5.x 前沿模型；日常使用从 medium reasoning 起步，复杂场景再提高 reasoning。

原因是这个 skill 不只是文本问答，经常需要：

- 读取练习卷照片、孩子手写答案、老师批改痕迹和几何图形；
- 判断手写不清、照片裁切、题目缺失等情况，并标记 `need-confirmation`，而不是硬猜；
- 跨 `memory/`、`records/`、`mistakes/`、`weak-points/` 对比历史薄弱项和复发情况；
- 稳定生成 `worksheet-spec.json`、可打印 HTML、答案、批改标准和诊断记录；
- 处理复杂应用题、几何题、期中/期末复习规划，以及“会做同类题但换问法就错”的迁移失败。

不建议用小型纯文本模型做拍照批改、几何图形题、复杂应用题或长期记忆更新。小模型可以用于提醒、整理格式、更新清单这类低风险任务。

## 学习工作区

建议在个人学习项目中使用以下结构：

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

## 初始化个人学习仓库

本仓库是通用 skill，不保存真实使用过程中产生的数据。每个家庭/学生应使用自己的个人学习仓库保存学习档案和练习卷产物。

个人学习仓库可以是 public，也可以是 private。若选择 public，需要更严格地控制哪些内容进入 `site/`，并避免提交敏感原始资料。

推荐结构：

```text
zhizhi-math-learning-data/
  README.md
  .gitignore
  curriculum/
  knowledge-points/
  memory/
  mistakes/
  records/
  weak-points/
  worksheets/
  site/
```

从 ClawHub 安装 skill 后初始化个人学习仓库：

```bash
mkdir zhizhi-math-learning-data
cd zhizhi-math-learning-data
git init
openclaw skills install zhizhi-math-coach
python3 skills/zhizhi-math-coach/scripts/init_learning_workspace.py \
  --workspace . \
  --student-name "孩子" \
  --school-entry-year 2025 \
  --grade 一年级 \
  --semester 下学期 \
  --textbook-edition 人教版 \
  --textbook-volume 一年级下册
git add .
git commit -m "Initialize math learning workspace"
git remote add origin git@github.com:<user>/zhizhi-math-learning-data.git
git push -u origin main
```

生成的 `.gitignore` 默认忽略 `skills/`，避免把 ClawHub 下载的 skill bundle 提交到个人学习仓库。换机器使用时重新安装 skill 即可。如果第一次 `git push` 失败，本地学习工作区仍然可以正常使用；先在当前 OpenClaw 机器上完成 GitHub 授权，再重试同步。

## GitHub 授权与同步

OpenClaw 运行的机器不一定安装了 GitHub CLI，也不一定已经登录 GitHub。有些 OpenClaw 供应商也不一定提供 GitHub token 环境变量配置入口。同步只依赖普通 `git`、正确的 remote，以及当前机器具备 push 权限。`gh` 命令是可选项，不是必需项。

优先推荐使用 GitHub Deploy key。交互方式是：OpenClaw 生成当前个人学习仓库专用的 SSH 公钥，通过飞书或 OpenClaw 回复发给家长；家长把公钥添加到对应 GitHub 仓库的 Settings -> Deploy keys，并勾选 `Allow write access`。

```bash
python3 skills/zhizhi-math-coach/scripts/prepare_github_deploy_key.py \
  --workspace . \
  --configure-remote
```

如果个人学习仓库还没有配置 `origin`，可以显式传入目标仓库：

```bash
python3 skills/zhizhi-math-coach/scripts/prepare_github_deploy_key.py \
  --workspace . \
  --github-owner <user> \
  --repo zhizhi-math-learning-data \
  --configure-remote
```

OpenClaw 应只发送脚本输出中的公钥，不发送私钥。飞书消息建议写清楚：

```text
请把下面这个 OpenClaw 公钥加入 GitHub 仓库：
位置：Settings -> Deploy keys -> Add deploy key
权限：勾选 Allow write access
添加后回复“已添加”，我会继续检查并发布。
```

家长添加后，再运行：

```bash
python3 skills/zhizhi-math-coach/scripts/check_git_sync.py --workspace . --check-push
```

第一次在个人学习仓库中使用 skill 时，如果发现还没有 GitHub 同步能力，回复里应该简短提示这个 Deploy key 授权流程。后续生成试卷并要求发布、发链接、push 或同步时，如果预检发现没有权限，也应该先返回本地文件路径，并再次发送 Deploy key 授权引导，而不是把出卷任务判定为失败。

如果不能使用 Deploy key 或 SSH，可以为个人学习仓库创建 fine-grained GitHub personal access token：

- 创建入口：GitHub 网页 -> 头像 -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens -> Generate new token。
- Repository access：只选择个人学习仓库，例如 `zhizhi-math-learning-data`。
- 日常同步权限：`Contents: Read and write`。
- 可选 workflow 权限：只有需要提交 `.github/workflows/pages.yml` 时，才额外授予 `Workflows: Read and write`。
- 可选 Pages API 权限：只有自动化要通过 GitHub API 配置 Pages 时，才额外授予 `Pages: Read and write`。如果家长在 GitHub Settings 页面手动开启 Pages，不需要这个权限。

HTTPS token 使用方式：

```bash
git remote set-url origin https://github.com/<user>/zhizhi-math-learning-data.git
git push --dry-run origin HEAD
```

当 Git 提示输入凭据时，用户名填 GitHub 用户名，密码位置填 token。不要把 token 粘贴到 OpenClaw 对话里，也不要写入仓库文件或 remote URL。

## 本地更新和同步如何触发

默认没有后台自动同步。

当 OpenClaw 在个人学习仓库中工作，并且用户触发 skill 时，才会读写本地学习文件。例如：

```text
$zhizhi-math-coach 批改这张练习卷，记录薄弱项。
$zhizhi-math-coach 根据最近错题生成变式练习。
```

常见写入触发点：

- 批改或诊断会更新 `records/`、`mistakes/`、`weak-points/`，必要时更新 `memory/`；
- 出卷会更新 `worksheets/<date-topic>/worksheet-spec.json`、`worksheet.html` 和 `answer-key.md`；
- 发布学生版页面会更新 `site/` 和 `worksheets/<date-topic>/publish.json`；
- OpenClaw 定时任务默认只提醒或建议，不自动写学习记录，也不自动出卷，除非家长明确要求。

同步到 GitHub 只在用户明确要求同步、push、发布、发链接，或用户自己在个人学习仓库里执行 Git 提交和推送时发生。OpenClaw 提交或推送前应先运行：

```bash
python3 skills/zhizhi-math-coach/scripts/check_git_sync.py --workspace . --check-push
```

如果预检失败，本地生成文件仍然有效；完成 SSH 或 token 授权后可以重试同步。

若个人学习仓库是 private，可以同步完整学习状态：

```bash
git add curriculum knowledge-points memory mistakes records weak-points worksheets site
git commit -m "Update learning records"
git push
```

若个人学习仓库是 public，只提交适合公开的文件。多数情况下只提交 `site/`，或提交已脱敏、无答案、无学生身份信息的练习卷文件。

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

## 从个人仓库发布学生版 HTML

如果你接受练习卷公开访问，应在个人学习仓库中运行发布脚本，只把学生版 HTML 发布到该仓库的 `site/`：

```bash
python3 skills/zhizhi-math-coach/scripts/publish_html_site.py \
  worksheets \
  --workspace . \
  --base-url https://<user>.github.io/zhizhi-math-learning-data
```

脚本会生成：

- `site/index.html`：个人学习仓库中的公开练习卷列表。
- `site/worksheets/<slug>/index.html`：可查看和打印的学生版练习卷。
- `site/.nojekyll`：GitHub Pages 静态站点标记。
- `worksheets/<date-topic>/publish.json`：记录发布信息。

`site/index.html` 会扫描 `worksheets/` 下所有可公开的学生版练习卷，按日期倒序展示，不会只展示本次发布的一张。索引列包括日期、练习状态、练习卷标题、主题、年级、题量和完成情况。练习状态优先从 `worksheets/status.md` 推断；没有记录时默认显示为 `未练习`。

`site/` 只放学生可见内容。不要把答案、批改记录、长短期记忆、薄弱项历史、上传试卷、教材 PDF 或 OCR 内容放进去。

飞书里建议发送 GitHub Pages 链接，答案和批改标准不要放进公开发布的 `site/` 目录。

要在线访问这些页面，需要在个人学习仓库 Settings -> Pages 中启用 Pages，可选择 `site/` 目录或复制 `docs/personal-learning-repo-template.md` 中的 workflow。

如果你的 GitHub Pages 页面提示 private repo 需要升级，可以把个人学习仓库改成 public 使用免费 Pages，但要明确：public 仓库里所有已提交文件都可被查看，不只是 `site/`。非协作者默认不能编辑 public 仓库，所以“别人可以看试卷”不等于“别人可以改 main”。建议不要添加协作者，并在 Settings -> Branches 或 Rulesets 中保护 `main`，至少禁止 force push 和删除分支；如果希望 OpenClaw 直接 push `site/` 和 workflow，不要启用会阻断 direct push 的强制 PR 规则。

推荐 GitHub Pages 设置：

1. Settings -> Pages -> Build and deployment -> Source 选择 `GitHub Actions`。
2. 在个人学习仓库新增 `.github/workflows/pages.yml`。
3. 如果 OpenClaw 已经通过 Deploy key 获得写权限，可以直接创建、提交并 push：

```bash
python3 skills/zhizhi-math-coach/scripts/setup_github_pages_workflow.py --workspace .
git add .github/workflows/pages.yml site
git commit -m "Configure GitHub Pages publishing"
git push
```

推荐 ruleset 配置：

- Ruleset name：`main protect`
- Enforcement status：`Active`
- Bypass list：
  - `Deploy keys`：`Always allow`
  - `Repository admin`：`Always allow`
- Target branches：`main`，或者默认分支就是 `main` 时选择 `Default`
- 勾选：
  - `Restrict updates`
  - `Restrict deletions`
  - `Block force pushes`
- 不勾选：
  - `Require a pull request before merging`
  - `Require status checks to pass`
  - `Require signed commits`
  - `Require deployments to succeed`

这样 public 仓库仍然可以被查看，但只有 deploy key 和仓库管理员能更新 `main`；OpenClaw 仍然可以直接 push，不需要每次开 PR、人工合并。

自动发布流程：

- 当个人学习仓库已经配置 public Pages、`.github/workflows/pages.yml` 和可写 Deploy key 后，skill 生成新练习卷时会自动发布学生版页面。
- OpenClaw 会先生成本地 `worksheet.html` 和 `answer-key.md`，再刷新 `site/`，提交并 push public-safe 文件。
- GitHub Actions 执行完成后，OpenClaw 再回复 Pages 首页链接和本次练习卷链接。
- 如果 Actions 失败或超时，本地文件仍然有效，OpenClaw 会返回本地路径和 Actions/授权排查信息。

可手动运行同一流程：

```bash
python3 skills/zhizhi-math-coach/scripts/publish_and_wait_pages.py \
  worksheets/<date-topic> \
  --workspace . \
  --base-url https://<user>.github.io/zhizhi-math-learning-data
```

## 教材使用边界

本项目可以使用教材信息帮助判断年级、册别、单元范围和知识点顺序。例如，个人学习工作区可以引用 `TapXWorld/ChinaTextbook` 中的人教版小学数学目录作为外部参考。

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
- 个人错题本、学习记录、记忆文件、教材进度或知识点笔记；
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
