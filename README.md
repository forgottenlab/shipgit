# 🚢 ShipGit

> **A lightweight Git publishing assistant for safe commits, version tags, and multi-remote pushes.**  
> **一个轻量级 Git 发布助手，支持安全提交、版本 Tag 和多远程仓库推送。**

<p align="center">
  <strong>ShipGit = Ship your Git project safely, clearly, and efficiently.</strong><br>
  <strong>ShipGit = 更安全、更清晰、更省心地发布你的 Git 项目。</strong>
</p>

---

## ✨ Overview / 项目简介

**ShipGit** is a lightweight command-line tool designed to simplify common Git publishing workflows.

It helps developers check Git project status, initialize repositories, manage `.gitignore`, configure remotes, inspect changed files, create commits and version tags, and push code to one or multiple remote repositories such as GitHub and Gitee.

**ShipGit** 是一个轻量级命令行工具，用于简化常见的 Git 发布流程。

它可以帮助开发者检查 Git 项目状态、初始化仓库、管理 `.gitignore`、配置远程仓库、查看变更文件、创建提交和版本 Tag，并将代码推送到 GitHub、Gitee 或其他远程仓库。

ShipGit is not intended to replace Git. Instead, it acts as a **guided assistant** on top of Git, making common publishing tasks easier and safer.

ShipGit 并不是为了取代 Git，而是在 Git 之上提供一个更加友好的**发布流程助手**，让常见发布任务更简单、更安全。

---

## 🎯 Why ShipGit? / 为什么需要 ShipGit？

When managing personal or open-source projects, developers often need to repeat similar Git operations:

开发个人项目或开源项目时，开发者经常需要重复执行类似的 Git 操作：

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
- 🏷️ You need to create version tags regularly  
  你需要经常创建版本 Tag
- 🛡️ You want to avoid accidentally committing build outputs or sensitive files  
  你想避免误提交构建产物或敏感文件
- 🧭 You want a guided workflow instead of remembering every command  
  你希望有一个流程化引导，而不是每次都手动记命令

ShipGit aims to make this process clearer and more reliable.

ShipGit 的目标就是让这个过程更清晰、更可靠。

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
- 🧪 **Basic regression test scripts** / 基础回归测试脚本
- 🧭 **Built-in quick guide** / 内置基础指引

---

## 📦 Installation / 安装方式

### Development install / 开发模式安装

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
ShipGit 0.1.0-prototype
```

---

## ⚡ Quick Start / 快速开始

### Show quick guide / 查看基础指引

```bash
shipgit guide
```

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

ShipGit provides basic regression test scripts.

ShipGit 提供了基础回归测试脚本。

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

## 🛣️ Roadmap / 后续计划

- ✅ Basic CLI structure / 基础 CLI 结构
- ✅ Project diagnosis / 项目诊断
- ✅ Status explanation / 状态码解释
- ✅ Language switching / 语言切换
- ✅ Basic regression tests / 基础回归测试
- 🔜 Improve publish workflow confirmation / 优化发布确认流程
- 🔜 Add SSH connectivity checks / 增加 SSH 连接检查
- 🔜 Add sensitive file scanning rules / 增强敏感文件扫描
- 🔜 Support one-line installation script / 支持一键安装脚本
- 🔜 Support packaging as standalone executable / 支持打包为独立可执行文件
- 🔜 Support GitHub and Gitee publishing templates / 支持 GitHub / Gitee 发布模板

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
│   └── i18n.py
├── scripts/
│   ├── test_shipgit.ps1
│   └── test_shipgit_isolated.ps1
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

## 🏷️ Version / 版本

Current prototype:

```text
v0.1.0-prototype
```

---

## 📜 License / 开源协议

License is not selected yet.

当前尚未选择开源协议。

---

## 🙌 Author / 作者

Created by [forgottenlab](https://github.com/forgottenlab).

由 [forgottenlab](https://github.com/forgottenlab) 创建。

