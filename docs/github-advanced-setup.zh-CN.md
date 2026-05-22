# GitHub 进阶配置：云同步与在线访问

这是一份给家长看的操作说明。默认情况下，你不需要配置 GitHub：OpenClaw 会把学习记录保存在当前工作区，并把新生成的练习卷作为 PDF 文件发给你。

只有当你想要下面这些能力时，才需要继续配置 GitHub：

- 云端保存 `learning-data`，避免只存在某一台 OpenClaw 机器上；
- 换机器后还能继续读取过去的学习记录；
- 生成一个在线链接，点开就能查看和打印练习卷；
- 让 OpenClaw 自动把练习数据同步到你的 GitHub 仓库。

## 你需要准备什么

你只需要准备一个 GitHub 账号。后面的命令由 OpenClaw 执行；你主要负责在 GitHub 网页上创建仓库、粘贴公钥、勾选权限。

推荐的个人学习仓库名：

```text
zhizhi-math-learning-data
```

这个仓库保存的是你的学习数据，不是 `zhizhi-math-coach` 技能源码。技能源码仓库是公开的通用能力包；个人学习仓库是每个家庭自己的数据仓库。

## 第一步：创建个人学习仓库

在浏览器打开 GitHub：

```text
https://github.com/new
```

按下面填写：

- Repository name：`zhizhi-math-learning-data`
- Description：可不填，或填 `Math learning data`
- Public / Private：都可以，按你的偏好选择
- 不要勾选 `Add a README file`
- 不要勾选 `.gitignore`
- 不要选择 license

点击 `Create repository`。

创建完成后，GitHub 页面上会显示仓库地址，类似：

```text
https://github.com/<你的GitHub用户名>/zhizhi-math-learning-data
```

记住你的 GitHub 用户名。后面 OpenClaw 会用到。

## 第二步：让 OpenClaw 初始化学习工作区

回到 OpenClaw，对它说：

```text
$zhizhi-math-coach 进阶：配置 GitHub 云同步

我的 GitHub 用户名是 <你的GitHub用户名>
我的学习数据仓库名是 zhizhi-math-learning-data
```

OpenClaw 应该做三件事：

1. 确认当前工作区是你的个人学习工作区，不是 `zhizhi-math-coach-openclaw` 技能源码仓库；
2. 如果学习目录还没有初始化，就创建 `memory/`、`curriculum/`、`worksheets/`、`records/` 等目录；
3. 生成一段 SSH public key，并发给你。

你会收到类似下面这样的内容：

```text
这是 GitHub 进阶配置，用于云同步 learning-data 和 Pages 在线访问。普通出卷仍会直接返回 PDF，不需要 GitHub。

SSH public key：
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... openclaw-zhizhi-math-coach-xxx

详细引导：
https://github.com/linzi007/zhizhi-math-coach-openclaw/blob/main/docs/github-advanced-setup.zh-CN.md

请在 GitHub 仓库中打开：
Settings -> Deploy keys -> Add deploy key

勾选 Allow write access。添加后回复“已添加”，我会继续检查并同步。
```

你只需要复制 `ssh-ed25519 ...` 这一整行公钥。不要复制任何私钥；OpenClaw 也不应该把私钥发给你。

## 第三步：把公钥加到 GitHub

打开你的个人学习仓库页面：

```text
https://github.com/<你的GitHub用户名>/zhizhi-math-learning-data
```

按下面点：

```text
Settings -> Deploy keys -> Add deploy key
```

填写：

- Title：`OpenClaw zhizhi-math-coach`
- Key：粘贴 OpenClaw 发给你的 `ssh-ed25519 ...` 公钥
- 勾选：`Allow write access`

然后点击 `Add key`。

如果 GitHub 要求你输入密码或二次验证，按 GitHub 页面提示完成即可。

## 第四步：告诉 OpenClaw 已添加

回到 OpenClaw，回复：

```text
已添加
```

OpenClaw 会检查当前机器是否已经能写入你的 GitHub 仓库。检查通过后，它会把当前学习工作区同步到 GitHub。

如果检查失败，不代表学习数据丢失。PDF、记录和练习卷仍在本地工作区里。失败时把 OpenClaw 返回的错误发出来，它会继续引导你处理。

## 第五步：开启 GitHub Pages 在线访问

这一步是可选的。只有你想要“点开链接查看和打印练习卷”时才需要做。

打开个人学习仓库：

```text
https://github.com/<你的GitHub用户名>/zhizhi-math-learning-data
```

按下面点：

```text
Settings -> Pages
```

找到 `Build and deployment`：

- Source：选择 `GitHub Actions`

然后回到 OpenClaw，说：

```text
$zhizhi-math-coach 进阶：开启 GitHub Pages 在线访问
```

OpenClaw 会创建 GitHub Pages 所需的 workflow 文件，并提交到你的个人学习仓库。

之后当你要求“发布在线链接”时，OpenClaw 会先返回 PDF，再发布在线页面。页面地址通常是：

```text
https://<你的GitHub用户名>.github.io/zhizhi-math-learning-data/
```

某一张练习卷的地址通常是：

```text
https://<你的GitHub用户名>.github.io/zhizhi-math-learning-data/worksheets/<练习卷目录名>/
```

## 第六步：保护 main 分支

如果你的个人学习仓库是 public，别人可以看，但默认不能修改。为了更稳妥，建议做一个保护规则。

打开个人学习仓库：

```text
Settings -> Rules -> Rulesets -> New ruleset -> New branch ruleset
```

按下面填写：

- Ruleset name：`main protect`
- Enforcement status：`Active`
- Target branches：选择 `main`，或选择默认分支

找到 Bypass list，添加：

- `Deploy keys`：`Always allow`
- `Repository admin`：`Always allow`

勾选这些规则：

- `Restrict updates`
- `Restrict deletions`
- `Block force pushes`

不要勾选这些规则：

- `Require a pull request before merging`
- `Require status checks to pass`
- `Require signed commits`
- `Require deployments to succeed`

这样可以做到：别人能看，不能改；OpenClaw 仍然可以通过 Deploy key 自动同步。

## 常用触发语

普通出卷，不需要 GitHub：

```text
$zhizhi-math-coach 根据最近错题生成变式练习，并返回 PDF。
```

配置云同步：

```text
$zhizhi-math-coach 进阶：配置 GitHub 云同步
```

生成或重新发送公钥：

```text
$zhizhi-math-coach 生成 GitHub Deploy key
```

开启在线访问：

```text
$zhizhi-math-coach 进阶：开启 GitHub Pages 在线访问
```

发布本次练习卷链接：

```text
$zhizhi-math-coach 发布这张练习卷到 GitHub Pages，并返回链接。
```

## 常见问题

### 不配置 GitHub 能不能用？

可以。默认就是本地学习记录 + PDF 文件回复。

### Public 仓库会不会被别人修改？

非协作者默认不能修改你的 public 仓库。public 的意思是别人可以看，不等于别人可以改。

### 为什么不用 GitHub token？

OpenClaw 运行环境不一定方便保存 token。Deploy key 更适合这个场景：只给某一个个人学习仓库授权，不影响你的其他仓库。

### `Allow write access` 是什么？

它允许 OpenClaw 把学习记录和练习卷提交到这个仓库。如果不勾选，OpenClaw 只能读取，不能同步。

### 我误把公钥加错仓库了怎么办？

到那个仓库的 `Settings -> Deploy keys` 删除它，然后在正确的个人学习仓库重新添加。

### GitHub Pages 是必须的吗？

不是。Pages 只是为了得到在线链接。普通打印和飞书发送 PDF 不需要 Pages。
