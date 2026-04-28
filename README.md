# 🚢 ShipGit

> **A lightweight Git publishing assistant for safe commits, version tags, multi-remote pushes, and local self-tests.**  
> **一个轻量级 Git 发布助手，支持安全提交、版本 Tag、多远程仓库推送与本地自检。**

<p align="center">
  <strong>ShipGit = Ship your Git project safely, clearly, and efficiently.</strong><br>
  <strong>ShipGit = 更安全、更清晰、更省心地发布你的 Git 项目。</strong>
</p>

<p align="center">
  <code>shipgit guide</code> · <code>shipgit test</code> · <code>shipgit doctor</code> · <code>shipgit publish</code>
</p>

---

## ✨ Overview / 项目简介

**ShipGit** is a lightweight command-line tool designed to simplify common Git publishing workflows.

It helps developers check Git project status, initialize repositories, manage `.gitignore`, configure remotes, inspect changed files, create commits and version tags, and push code to one or multiple remote repositories such as GitHub and Gitee.

**ShipGit** 是一个轻量级命令行工具，用于简化常见的 Git 发布流程。

它可以帮助开发者检查 Git 项目状态、初始化仓库、管理 `.gitignore`、配置远程仓库、查看变更文件、创建提交和版本 Tag，并将代码推送到 GitHub、Gitee 或其他远程仓库。

ShipGit is not intended to replace Git. Instead, it acts as a **guided assistant** on top of Git, making common publishing tasks easier, clearer, and safer.

ShipGit 并不是为了取代 Git，而是在 Git 之上提供一个更加友好的**发布流程助手**，让常见发布任务更简单、更清晰、更安全。

---

## 🎯 Why ShipGit? / 为什么需要 ShipGit？

When managing personal, coursework, or open-source projects, developers often repeat similar Git operations:

开发个人项目、课程项目或开源项目时，开发者经常需要重复执行类似的 Git 操作：

```bash
git status
git add .
git commit -m "feat: update project"
git tag v0.1.0
git push github main
git push gitee main
git push github v0.1.0
git push gitee v0.1.0
```

This process is not difficult, but it is easy to make mistakes, especially when:

这个流程本身不复杂，但很容易出错，尤其是在以下场景中：

- 🧩 You manage multiple remotes, such as GitHub and Gitee  
  你需要同时维护 GitHub、Gitee 等多个远程仓库
- 🏷️ You need to create and push version tags regularly  
  你需要经常创建并推送版本 Tag
- 🛡️ You want to avoid accidentally committing build outputs or sensitive files  
  你想避免误提交构建产物或敏感文件
- 🧭 You want a guided workflow instead of remembering every command  
  你希望有一个流程化引导，而不是每次都手动记命令
- 🧪 You want users to verify the installation quickly after installing  
  你希望用户安装后可以快速验证工具是否可用

ShipGit aims to make Git publishing clearer, safer, and easier to repeat.

ShipGit 的目标就是让 Git 发布流程更清晰、更安全、更容易复现。

---

## 🚀 Features / 功能特性

- 🔍 **Git project diagnosis** / Git 项目诊断
- 📄 **`.gitignore` detection and creation** / `.gitignore` 检查与创建
- 👤 **Git user configuration check** / Git 用户信息检查
- 📊 **Changed file status explanation** / 变更文件状态说明
- 🌐 **Remote repository management** / 远程仓库管理
- 📝 **Commit and tag workflow** / 提交与 Tag 流程
- 🔁 **Multi-remote publishing** / 多远程仓库推送
- 🌏 **Chinese, English, and bilingual output** / 中文、英文、双语输出
- 🧭 **Built-in quick guide** / 内置基础指引
- 🧪 **Built-in self-test command** / 内置自检命令
- 📦 **PowerShell installer, updater, and uninstaller scripts** / PowerShell 安装、更新、卸载脚本
- 🧰 **Regression and distribution test scripts** / 回归测试与分发测试脚本

---

## 📦 Installation / 安装方式

### ✅ Recommended: Windows PowerShell one-line install / 推荐：Windows PowerShell 一键安装

```powershell
irm https://raw.githubusercontent.com/forgottenlab/shipgit/main/scripts/install.ps1 | iex
```

After installation, restart PowerShell if necessary, then run:

安装完成后，如有需要请重启 PowerShell，然后运行：

```powershell
shipgit -v
shipgit guide
shipgit test
```

### 🔒 Safer install / 更安全的安装方式

If you want to review the installer before running it:

如果你希望先查看安装脚本内容再执行：

```powershell
irm https://raw.githubusercontent.com/forgottenlab/shipgit/main/scripts/install.ps1 -OutFile install.ps1
Get-Content .\install.ps1
.\install.ps1
```

### 🔁 Update / 更新

Run the installer again:

再次运行安装脚本即可更新：

```powershell
irm https://raw.githubusercontent.com/forgottenlab/shipgit/main/scripts/install.ps1 | iex
```

Or run the updater script inside the repository:

也可以在仓库目录中运行更新脚本：

```powershell
.\scripts\update.ps1
```

### 🗑️ Uninstall / 卸载

If ShipGit was installed by `pipx`, uninstall it with:

如果 ShipGit 是通过 `pipx` 安装的，可以使用：

```powershell
python -m pipx uninstall shipgit
```

Or run the repository uninstall script:

也可以运行仓库中的卸载脚本：

```powershell
.\scripts\uninstall.ps1
```

### 🧑‍💻 Development install / 开发模式安装

Clone the repository:

```bash
git clone git@github.com:forgottenlab/shipgit.git
cd shipgit
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install ShipGit in editable mode:

```bash
pip install -e .
```

Check version:

```bash
shipgit -v
```

Expected output:

```text
ShipGit 0.1.1-prototype
```

---

## 🔐 Privacy and Security / 隐私与安全说明

ShipGit does **not** collect or upload:

ShipGit **不会**收集或上传：

- Machine IDs / 机器码
- Hardware serial numbers / 硬件序列号
- GitHub tokens / GitHub Token
- SSH private keys / SSH 私钥
- Personal files / 用户个人文件
- Browser data / 浏览器数据
- Clipboard content / 剪贴板内容

The installer only checks whether Python, Git, and `pipx` are available, then installs or updates ShipGit locally.

安装脚本只会检查 Python、Git、`pipx` 是否可用，然后在本地安装或更新 ShipGit。

> ⚠️ As with any `irm ... | iex` command, you should only run scripts from repositories you trust.  
> ⚠️ 和所有 `irm ... | iex` 命令一样，请只运行你信任的仓库中的脚本。

---

## ⚡ Quick Start / 快速开始

### Show quick guide / 查看基础指引

```bash
shipgit guide
```

### Run self-test / 运行自检测试

```bash
shipgit test
```

The self-test creates a temporary Git project and verifies ShipGit initialization, status detection, remote configuration, and config loading. It does **not** push anything to the network.

自检测试会创建一个临时 Git 项目，并验证 ShipGit 初始化、状态检测、远程仓库配置和配置文件读取。它**不会**向网络推送任何内容。

### Diagnose current project / 诊断当前项目

```bash
shipgit doctor
```

### Show changed files / 查看变更文件

```bash
shipgit status
```

### Initialize a project / 初始化项目

```bash
shipgit init
```

### Add a remote repository / 添加远程仓库

```bash
shipgit remote-add github git@github.com:your-name/your-repo.git
```

### List remotes / 查看远程仓库

```bash
shipgit remote-list
```

### Publish interactively / 交互式发布

```bash
shipgit publish
```

### Publish with commit message and tag / 指定提交说明和 Tag 发布

```bash
shipgit publish -m "feat: update project" -t v0.1.0 --all-remotes
```

---

## 🌏 Language / 语言设置

ShipGit supports Chinese, English, and bilingual output.

ShipGit 支持中文、英文和双语输出。

### Set default language / 设置默认语言

```bash
shipgit config-lang zh
shipgit config-lang en
shipgit config-lang bi
```

### Temporarily override language / 临时切换语言

```bash
shipgit doctor --lang en
shipgit --lang bi status
shipgit test --lang en
```

### Supported language values / 支持的语言值

```text
zh = Chinese / 中文
en = English / 英文
bi = Bilingual / 双语
```

---

## 🧭 Commands / 命令说明

| Command | Description | 中文说明 |
|---|---|---|
| `shipgit guide` | Show quick guide | 显示基础使用指引 |
| `shipgit test` | Run self-test in a temporary project | 创建临时项目并运行自检测试 |
| `shipgit doctor` | Check Git project status and risks | 检查 Git 项目状态和风险项 |
| `shipgit status` | Show changed files and explain Git status codes | 查看变更文件并解释 Git 状态码 |
| `shipgit init` | Initialize Git repository and ShipGit config | 初始化 Git 仓库和 ShipGit 配置 |
| `shipgit remote-add <name> <url>` | Add or update a remote repository | 添加或更新远程仓库 |
| `shipgit remote-list` | List configured remotes | 查看远程仓库列表 |
| `shipgit publish` | Commit, tag, and push changes interactively | 交互式提交、打 Tag、推送 |
| `shipgit config-lang zh\|en\|bi` | Set default language | 设置默认语言 |
| `shipgit version` | Show version | 查看版本号 |
| `shipgit -v` | Show version | 查看版本号 |
| `shipgit --version` | Show version | 查看版本号 |

---

## 🧪 Testing / 测试

ShipGit provides multiple levels of tests.

ShipGit 提供多层级测试方式。

### Built-in self-test / 内置自检

```powershell
shipgit test
shipgit test --lang en
shipgit --lang bi test
```

This is the recommended first check for users after installation.

这是推荐用户安装后首先运行的检查命令。

### Basic regression test / 基础回归测试

```powershell
.\scripts\test_shipgit.ps1
```

This script checks common commands such as:

该脚本会测试常见命令，例如：

- `shipgit version`
- `shipgit -v`
- `shipgit --version`
- `shipgit guide`
- `shipgit test`
- `shipgit doctor`
- `shipgit status`
- `shipgit init`
- `shipgit remote-list`

### Isolated regression test / 隔离回归测试

```powershell
.\scripts\test_shipgit_isolated.ps1
```

The isolated test creates a temporary Git project, runs ShipGit commands, verifies remote configuration, and removes the temporary directory after testing.

隔离测试会创建一个临时 Git 项目，执行 ShipGit 命令，验证远程仓库配置，并在测试结束后删除临时目录。

### Distribution test: local source / 分发测试：本地源码

```powershell
.\scripts\test_distribution.ps1 -LocalSource -Yes
```

This test installs, updates, verifies, and uninstalls ShipGit with `pipx` from the current local repository.

该测试会从当前本地仓库使用 `pipx` 安装、更新、验证并卸载 ShipGit。

### Distribution test: GitHub source / 分发测试：GitHub 源

```powershell
.\scripts\test_distribution.ps1 -Yes
```

This test installs, updates, verifies, and uninstalls ShipGit with `pipx` from the GitHub repository.

该测试会从 GitHub 仓库使用 `pipx` 安装、更新、验证并卸载 ShipGit。

> For cleaner distribution testing, use a fresh PowerShell session without activating Conda.  
> 为了更干净地测试分发安装，建议在未激活 Conda 的全新 PowerShell 中运行。

---

## ⚙️ Configuration / 配置文件

ShipGit creates a `.shipgit.yml` file in the project root.

ShipGit 会在项目根目录创建 `.shipgit.yml` 配置文件。

Example:

```yaml
project:
  name: shipgit
  defaultBranch: main

ui:
  language: zh

remotes:
- name: github
  url: git@github.com:forgottenlab/shipgit.git
  enabled: true

publish:
  pushTags: true
  requireGitignore: true
```

---

## 📊 Git Status Codes / Git 状态码说明

ShipGit explains common Git status codes in a more readable way.

ShipGit 会将常见 Git 状态码解释为更容易理解的说明。

| Code | Meaning | 中文说明 |
|---|---|---|
| `??` | Untracked | 未跟踪 |
| `A` | Added | 新增 |
| `M` | Modified | 已修改 |
| `D` | Deleted | 已删除 |
| `R` | Renamed | 重命名 |
| `C` | Copied | 复制 |
| `U` | Unmerged / Conflict | 冲突 |
| `T` | Type changed | 类型变更 |
| `!!` | Ignored | 已忽略 |

---

## 🧱 Project Structure / 项目结构

```text
shipgit/
├── shipgit/
│   ├── __init__.py
│   ├── main.py
│   ├── git_runner.py
│   ├── config.py
│   ├── checks.py
│   ├── publisher.py
│   ├── guide.py
│   ├── tester.py
│   └── i18n.py
├── scripts/
│   ├── install.ps1
│   ├── update.ps1
│   ├── uninstall.ps1
│   ├── test_shipgit.ps1
│   ├── test_shipgit_isolated.ps1
│   └── test_distribution.ps1
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

## 🛣️ Roadmap / 后续计划

- ✅ Basic CLI structure / 基础 CLI 结构
- ✅ Project diagnosis / 项目诊断
- ✅ Status explanation / 状态码解释
- ✅ Language switching / 语言切换
- ✅ Built-in quick guide / 内置基础指引
- ✅ Built-in self-test command / 内置自检命令
- ✅ Basic regression tests / 基础回归测试
- ✅ Isolated regression tests / 隔离回归测试
- ✅ PowerShell install/update/uninstall scripts / PowerShell 安装、更新、卸载脚本
- ✅ Local distribution test / 本地源码分发测试
- 🔜 GitHub-source distribution test / GitHub 源分发测试
- 🔜 Improve publish workflow confirmation / 优化发布确认流程
- 🔜 Add SSH connectivity checks / 增加 SSH 连接检查
- 🔜 Add sensitive file scanning rules / 增强敏感文件扫描
- 🔜 Support packaging as standalone executable / 支持打包为独立可执行文件
- 🔜 Support GitHub and Gitee publishing templates / 支持 GitHub / Gitee 发布模板

---

## 🏷️ Version / 版本

Current prototype:

```text
v0.1.1-prototype
```

### Version notes / 版本说明

`v0.1.1-prototype` adds:

`v0.1.1-prototype` 新增：

- Built-in `shipgit test` self-test command / 内置 `shipgit test` 自检命令
- PowerShell installer / PowerShell 安装脚本
- PowerShell updater / PowerShell 更新脚本
- PowerShell uninstaller / PowerShell 卸载脚本
- Distribution test workflow / 分发安装测试流程
- Improved quick guide / 改进基础指引
- Privacy and installation notes / 增加隐私与安装说明

---

## 📜 License / 开源协议

License is not selected yet.

当前尚未选择开源协议。

---

## 🙌 Author / 作者

Created by [forgottenlab](https://github.com/forgottenlab).

由 [forgottenlab](https://github.com/forgottenlab) 创建。
