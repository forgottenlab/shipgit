from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from shipgit.i18n import text, cell_text, title_text


console = Console()


def show_command_guide(lang: str = "zh") -> None:
    table = Table(
        title=title_text("ShipGit 基础指引", "ShipGit Quick Guide", lang),
        box=box.SQUARE,
        show_lines=True,
        expand=False,
    )

    table.add_column("No.", style="magenta", width=4, justify="right")
    table.add_column(cell_text("命令", "Command", lang), style="cyan", min_width=22)
    table.add_column(cell_text("用途", "Description", lang), min_width=42)

    rows = [
        ("1", "shipgit guide", cell_text("显示基础使用指引", "Show this quick guide", lang)),
        ("2", "shipgit test", cell_text("创建临时项目并运行 ShipGit 自检测试", "Create a temporary project and run ShipGit self-test", lang)),
        ("3", "shipgit doctor", cell_text("检查当前项目的 Git 状态、配置和风险项", "Check Git status, configuration, and risks", lang)),
        ("4", "shipgit status", cell_text("查看当前变更文件，并解释 Git 状态码", "Show changed files and explain Git status codes", lang)),
        ("5", "shipgit init", cell_text("初始化 Git 仓库并创建 ShipGit 配置", "Initialize Git repository and ShipGit config", lang)),
        ("6", "shipgit remote-list", cell_text("查看当前项目配置的远程仓库", "List configured Git remotes", lang)),
        ("7", "shipgit remote-add <name> <url>", cell_text("添加或更新远程仓库，例如 GitHub / Gitee", "Add or update a remote, such as GitHub / Gitee", lang)),
        ("8", "shipgit publish", cell_text("交互式提交、打 tag、推送到远程仓库", "Interactively commit, tag, and push to remotes", lang)),
        ("9", "shipgit config-lang zh|en|bi", cell_text("设置当前项目默认语言", "Set default language for current project", lang)),
        ("10", "shipgit -v", cell_text("查看版本号", "Show version", lang)),
    ]

    for row in rows:
        table.add_row(*row)

    console.print(table)

    console.print(
        Panel(
            text(
                "提示：大多数命令都支持 `--lang zh|en|bi` 临时切换语言。",
                "Tip: Most commands support `--lang zh|en|bi` to temporarily switch language.",
                lang,
            ),
            title=title_text("使用提示", "Usage Tip", lang),
            border_style="cyan",
        )
    )

    console.print(
        Panel(
            text(
                "安装：运行 scripts/install.ps1 或 README 中的一键安装命令。\n更新：重新运行安装脚本即可。\n卸载：运行 scripts/uninstall.ps1 或 py -m pipx uninstall shipgit。",
                "Install: run scripts/install.ps1 or the one-line command in README.\nUpdate: run the installer again.\nUninstall: run scripts/uninstall.ps1 or py -m pipx uninstall shipgit.",
                lang,
            ),
            title=title_text("安装 / 更新 / 卸载", "Install / Update / Uninstall", lang),
            border_style="green",
        )
    )
