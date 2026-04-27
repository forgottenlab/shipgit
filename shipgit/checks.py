from __future__ import annotations

from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from shipgit.git_runner import run_git
from shipgit.i18n import text, cell_text, title_text, status_text


console = Console()


DEFAULT_GITIGNORE = """# Build outputs
target/
build/
dist/
out/

# IDE
.idea/
.vscode/
*.iml

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Env and secrets
.env
.env.*
*.key
*.pem
id_rsa
id_ed25519
application-prod.yml
application-secret.yml

# Python
__pycache__/
*.pyc
.venv/
venv/

# Node
node_modules/
"""


SENSITIVE_PATTERNS = [
    ".env",
    "id_rsa",
    "id_ed25519",
    "application-prod.yml",
    "application-secret.yml",
    ".pem",
    ".key",
]


def is_git_repo(project_dir: Path) -> bool:
    result = run_git(project_dir, ["rev-parse", "--is-inside-work-tree"])
    return result.ok and result.stdout.strip() == "true"


def ensure_gitignore(project_dir: Path, create_if_missing: bool = True) -> bool:
    gitignore = project_dir / ".gitignore"

    if gitignore.exists():
        return True

    if create_if_missing:
        gitignore.write_text(DEFAULT_GITIGNORE, encoding="utf-8")
        return True

    return False


def get_current_branch(project_dir: Path) -> str:
    result = run_git(project_dir, ["branch", "--show-current"])
    if result.ok and result.stdout:
        return result.stdout.strip()
    return "main"


def get_git_status(project_dir: Path) -> list[str]:
    result = run_git(project_dir, ["status", "--porcelain"])
    if not result.ok or not result.stdout:
        return []
    return result.stdout.splitlines()


def get_remotes(project_dir: Path) -> dict[str, str]:
    result = run_git(project_dir, ["remote", "-v"])
    remotes: dict[str, str] = {}

    if not result.ok or not result.stdout:
        return remotes

    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            name = parts[0]
            url = parts[1]
            remotes[name] = url

    return remotes


def check_git_user(project_dir: Path) -> tuple[str, str]:
    name_result = run_git(project_dir, ["config", "--global", "user.name"])
    email_result = run_git(project_dir, ["config", "--global", "user.email"])

    name = name_result.stdout.strip() if name_result.ok else ""
    email = email_result.stdout.strip() if email_result.ok else ""

    return name, email


def scan_sensitive_files(project_dir: Path) -> list[str]:
    suspicious: list[str] = []

    for path in project_dir.rglob("*"):
        if ".git" in path.parts:
            continue

        if path.is_dir():
            continue

        relative = str(path.relative_to(project_dir)).replace("\\", "/")
        lower = relative.lower()

        for pattern in SENSITIVE_PATTERNS:
            if pattern.lower() in lower:
                suspicious.append(relative)
                break

    return suspicious


def print_doctor_report(project_dir: Path, lang: str = "zh") -> None:
    git_repo = is_git_repo(project_dir)
    gitignore_exists = (project_dir / ".gitignore").exists()
    git_user_name, git_user_email = check_git_user(project_dir)
    current_branch = get_current_branch(project_dir) if git_repo else "-"
    remotes = get_remotes(project_dir) if git_repo else {}
    status_lines = get_git_status(project_dir) if git_repo else []
    suspicious = scan_sensitive_files(project_dir)

    table = Table(
        title=title_text("ShipGit 项目诊断报告", "ShipGit Doctor Report", lang),
        box=box.SQUARE,
        show_lines=True,
        expand=False,
    )

    table.add_column("No.", style="magenta", no_wrap=True, width=4, justify="right")
    table.add_column(cell_text("检查项", "Check Item", lang), style="cyan", min_width=18, overflow="fold")
    table.add_column(cell_text("状态", "Status", lang), style="green", min_width=10, overflow="fold")
    table.add_column(cell_text("说明", "Detail", lang), min_width=32, overflow="fold")

    rows: list[tuple[str, str, str, str]] = [
        (
            "1",
            cell_text("Git 仓库", "Git repository", lang),
            status_text("ok" if git_repo else "missing", lang),
            cell_text(
                "已检测到 .git 目录" if git_repo else "当前目录尚未初始化为 Git 仓库",
                "Detected .git directory" if git_repo else "Current directory is not initialized as a Git repository",
                lang,
            ),
        ),
        (
            "2",
            cell_text("Git 忽略规则文件", ".gitignore", lang),
            status_text("ok" if gitignore_exists else "missing", lang),
            cell_text(
                ".gitignore 文件已存在" if gitignore_exists else "建议在第一次提交前创建 .gitignore 文件",
                ".gitignore exists" if gitignore_exists else "It is recommended to create .gitignore before the first commit",
                lang,
            ),
        ),
        (
            "3",
            cell_text("Git 用户名", "Git user.name", lang),
            status_text("ok" if git_user_name else "missing", lang),
            git_user_name or cell_text(
                '请执行：git config --global user.name "你的用户名"',
                'Run: git config --global user.name "your-name"',
                lang,
            ),
        ),
        (
            "4",
            cell_text("Git 邮箱", "Git user.email", lang),
            status_text("ok" if git_user_email else "missing", lang),
            git_user_email or cell_text(
                '请执行：git config --global user.email "你的邮箱"',
                'Run: git config --global user.email "your-email"',
                lang,
            ),
        ),
        (
            "5",
            cell_text("当前分支", "Current branch", lang),
            status_text("ok" if current_branch else "unknown", lang),
            current_branch if current_branch else cell_text(
                "尚未检测到当前分支",
                "Current branch not detected",
                lang,
            ),
        ),
        (
            "6",
            cell_text("远程仓库", "Remotes", lang),
            status_text("ok" if remotes else "missing", lang),
            (
                cell_text("已配置：", "Configured: ", lang) + "\n" + ", ".join(sorted(remotes.keys()))
                if remotes
                else cell_text(
                    "尚未配置远程仓库，例如 GitHub / Gitee",
                    "No remote configured, e.g. GitHub / Gitee",
                    lang,
                )
            ),
        ),
        (
            "7",
            cell_text("工作区", "Working tree", lang),
            status_text("changed" if status_lines else "clean", lang),
            (
                cell_text(
                    f"检测到 {len(status_lines)} 个变更文件",
                    f"{len(status_lines)} changed file(s)",
                    lang,
                )
                if status_lines
                else cell_text("当前没有待提交变更", "No pending changes", lang)
            ),
        ),
        (
            "8",
            cell_text("敏感文件", "Sensitive files", lang),
            status_text("warning" if suspicious else "ok", lang),
            (
                cell_text(
                    f"检测到 {len(suspicious)} 个疑似敏感文件",
                    f"{len(suspicious)} suspicious file(s) detected",
                    lang,
                )
                if suspicious
                else cell_text(
                    "未发现明显的敏感文件",
                    "No obvious sensitive files found",
                    lang,
                )
            ),
        ),
    ]

    for row in rows:
        table.add_row(*row)

    console.print(table)

    if suspicious:
        console.print("")
        console.print(
            Panel(
                "\n".join([f"- {item}" for item in suspicious[:20]]),
                title=title_text("疑似敏感文件列表", "Suspicious files", lang),
                border_style="yellow",
            )
        )

    raw_suggestions: list[tuple[str, str]] = []

    if not git_repo:
        raw_suggestions.append(
            (
                "运行 `shipgit init` 初始化当前项目。",
                "Run `shipgit init` to initialize the current project.",
            )
        )

    if git_repo and not remotes:
        raw_suggestions.append(
            (
                "配置远程仓库，例如 GitHub / Gitee。",
                "Configure remotes, for example GitHub / Gitee.",
            )
        )

    if status_lines:
        raw_suggestions.append(
            (
                "当前存在未提交变更，可运行 `shipgit status` 或后续执行 publish。",
                "There are uncommitted changes. You can run `shipgit status` or publish later.",
            )
        )

    if raw_suggestions:
        suggestions = [
            text(f"{index}. {zh}", f"{index}. {en}", lang)
            for index, (zh, en) in enumerate(raw_suggestions, start=1)
        ]

        console.print("")
        console.print(
            Panel(
                "\n".join(suggestions),
                title=title_text("下一步建议", "Next Suggestions", lang),
                border_style="cyan",
            )
        )
