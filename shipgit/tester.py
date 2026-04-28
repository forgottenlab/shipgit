from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from shipgit.git_runner import run_git
from shipgit.checks import ensure_gitignore, is_git_repo, get_remotes, get_git_status
from shipgit.publisher import init_repo, add_remote
from shipgit.config import load_config
from shipgit.i18n import text, cell_text, title_text


console = Console()


def _add_result(
    table: Table,
    no: int,
    name_zh: str,
    name_en: str,
    passed: bool,
    detail_zh: str,
    detail_en: str,
    lang: str,
) -> None:
    table.add_row(
        str(no),
        cell_text(name_zh, name_en, lang),
        cell_text("通过" if passed else "失败", "PASS" if passed else "FAIL", lang),
        cell_text(detail_zh, detail_en, lang),
    )


def run_self_test(lang: str = "zh") -> bool:
    root = Path(tempfile.mkdtemp(prefix="shipgit-self-test-")).resolve()
    passed_all = True

    console.print(
        Panel(
            text(
                f"测试项目：{root}\n此测试不会向网络推送任何内容。",
                f"Test project: {root}\nThis test will not push anything to the network.",
                lang,
            ),
            title=title_text("ShipGit 自检测试", "ShipGit Self Test", lang),
            border_style="cyan",
        )
    )

    table = Table(
        title=title_text("测试结果", "Test Results", lang),
        box=box.SQUARE,
        show_lines=True,
        expand=False,
    )
    table.add_column("No.", style="magenta", width=4, justify="right")
    table.add_column(cell_text("测试项", "Test Item", lang), style="cyan", min_width=24)
    table.add_column(cell_text("结果", "Result", lang), style="green", min_width=10)
    table.add_column(cell_text("说明", "Detail", lang), min_width=40)

    try:
        (root / "README.md").write_text("hello shipgit self test\n", encoding="utf-8")

        init_repo(root, lang=lang)
        git_repo_ok = is_git_repo(root)
        passed_all = passed_all and git_repo_ok
        _add_result(
            table, 1,
            "初始化 Git 仓库", "Initialize Git repository",
            git_repo_ok,
            "已检测到 .git 目录", "Detected .git directory",
            lang,
        )

        ensure_gitignore(root, create_if_missing=True)
        gitignore_ok = (root / ".gitignore").exists()
        passed_all = passed_all and gitignore_ok
        _add_result(
            table, 2,
            "创建 .gitignore", "Create .gitignore",
            gitignore_ok,
            ".gitignore 文件已存在", ".gitignore exists",
            lang,
        )

        config = load_config(root)
        config_ok = config.project_name == root.name and config.default_branch in {"main", "master"}
        passed_all = passed_all and config_ok
        _add_result(
            table, 3,
            "读取 ShipGit 配置", "Load ShipGit config",
            config_ok,
            f"project={config.project_name}, branch={config.default_branch}",
            f"project={config.project_name}, branch={config.default_branch}",
            lang,
        )

        status_lines = get_git_status(root)
        status_ok = len(status_lines) >= 1
        passed_all = passed_all and status_ok
        _add_result(
            table, 4,
            "检查 Git 状态", "Check Git status",
            status_ok,
            f"检测到 {len(status_lines)} 个变更项",
            f"Detected {len(status_lines)} changed item(s)",
            lang,
        )

        remote_name = "local-test"
        remote_url = "https://example.com/example/shipgit-test.git"
        add_remote(root, remote_name, remote_url, lang=lang)
        remotes = get_remotes(root)
        remote_ok = remotes.get(remote_name) == remote_url
        passed_all = passed_all and remote_ok
        _add_result(
            table, 5,
            "添加远程仓库", "Add remote",
            remote_ok,
            f"{remote_name} -> {remote_url}",
            f"{remote_name} -> {remote_url}",
            lang,
        )

        git_remote_result = run_git(root, ["remote", "-v"])
        git_remote_ok = git_remote_result.ok and remote_name in git_remote_result.stdout
        passed_all = passed_all and git_remote_ok
        _add_result(
            table, 6,
            "验证 Git remote", "Verify Git remote",
            git_remote_ok,
            "git remote -v 输出正常",
            "git remote -v output is valid",
            lang,
        )

        console.print(table)

        if passed_all:
            console.print(
                Panel(
                    text("ShipGit 自检测试通过。", "ShipGit self-test passed.", lang),
                    title=title_text("完成", "Done", lang),
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    text(
                        "ShipGit 自检测试未完全通过，请检查上方失败项。",
                        "ShipGit self-test did not fully pass. Please check failed items above.",
                        lang,
                    ),
                    title=title_text("失败", "Failed", lang),
                    border_style="red",
                )
            )

        return passed_all

    finally:
        shutil.rmtree(root, ignore_errors=True)
