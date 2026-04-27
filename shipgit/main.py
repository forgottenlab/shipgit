from __future__ import annotations

from pathlib import Path
import typer
import questionary
from rich.console import Console
from rich.panel import Panel

from shipgit import __version__
from shipgit.i18n import set_lang, get_lang, normalize_lang, text
from shipgit.guide import show_command_guide
from shipgit.checks import (
    print_doctor_report,
    ensure_gitignore,
    is_git_repo,
    get_current_branch,
    get_remotes,
)
from shipgit.publisher import (
    init_repo,
    add_remote,
    print_status,
    publish,
)
from shipgit.config import (
    load_config,
    save_config,
    add_or_update_remote_config,
)


app = typer.Typer(
    name="shipgit",
    help="ShipGit - A lightweight Git shipping assistant.",
)

console = Console()
GLOBAL_LANG_OVERRIDE: str | None = None


def resolve_project_dir(path: str | None) -> Path:
    if path:
        project_dir = Path(path).expanduser().resolve()
    else:
        project_dir = Path.cwd().resolve()

    if not project_dir.exists():
        raise typer.BadParameter(f"Project directory does not exist: {project_dir}")

    if not project_dir.is_dir():
        raise typer.BadParameter(f"Path is not a directory: {project_dir}")

    return project_dir


def apply_language(project_dir: Path, command_lang: str | None = None) -> str:
    if command_lang:
        final_lang = normalize_lang(command_lang)
    elif GLOBAL_LANG_OVERRIDE:
        final_lang = normalize_lang(GLOBAL_LANG_OVERRIDE)
    else:
        config = load_config(project_dir)
        final_lang = normalize_lang(config.language)

    set_lang(final_lang)
    return final_lang


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    lang: str | None = typer.Option(
        None,
        "--lang",
        "-l",
        help="Language: zh / en / bi",
    ),
    version_flag: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show ShipGit version and exit.",
    ),
) -> None:
    global GLOBAL_LANG_OVERRIDE

    if lang:
        GLOBAL_LANG_OVERRIDE = normalize_lang(lang)
        set_lang(GLOBAL_LANG_OVERRIDE)

    if version_flag:
        console.print(f"ShipGit {__version__}")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        project_dir = Path.cwd().resolve()
        active_lang = apply_language(project_dir, lang)
        console.print(f"[bold]{text('ShipGit 命令行工具', 'ShipGit command line tool', active_lang)}[/bold]")
        show_command_guide(active_lang)


@app.command()
def guide(
    lang: str | None = typer.Option(None, "--lang", "-l", help="Language: zh / en / bi"),
) -> None:
    """
    Show ShipGit quick guide.
    """
    active_lang = apply_language(Path.cwd().resolve(), lang)
    show_command_guide(active_lang)


@app.command()
def version(
    lang: str | None = typer.Option(None, "--lang", "-l", help="Language: zh / en / bi"),
) -> None:
    """
    Show ShipGit version.
    """
    apply_language(Path.cwd().resolve(), lang)
    console.print(f"ShipGit {__version__}")


@app.command()
def doctor(
    path: str | None = typer.Argument(None, help="Project directory. Default: current directory."),
    lang: str | None = typer.Option(None, "--lang", "-l", help="Language: zh / en / bi"),
) -> None:
    """
    Check Git environment and project status.
    """
    project_dir = resolve_project_dir(path)
    active_lang = apply_language(project_dir, lang)

    console.print(f"[bold]{text('项目', 'Project', active_lang)}:[/bold] {project_dir}")
    print_doctor_report(project_dir, lang=active_lang)


@app.command()
def init(
    path: str | None = typer.Argument(None, help="Project directory. Default: current directory."),
    lang: str | None = typer.Option(None, "--lang", "-l", help="Language: zh / en / bi"),
) -> None:
    """
    Initialize ShipGit and Git repository.
    """
    project_dir = resolve_project_dir(path)
    active_lang = apply_language(project_dir, lang)

    console.print(
        Panel.fit(
            f"[bold]{text('正在初始化项目', 'Initializing project', active_lang)}:[/bold]\n{project_dir}"
        )
    )

    init_repo(project_dir, lang=active_lang)
    ensure_gitignore(project_dir, create_if_missing=True)

    config = load_config(project_dir)
    config.project_name = project_dir.name
    config.default_branch = get_current_branch(project_dir) or "main"

    # init 不应该因为 --lang 临时参数而改变项目默认语言。
    # 默认语言只由 shipgit config-lang 修改。
    if not config.language:
        config.language = "zh"

    save_config(project_dir, config)

    console.print(f"[green]{text('ShipGit 配置已创建或更新。', 'ShipGit config created or updated.', active_lang)}[/green]")
    console.print(f"[cyan]{text('配置文件', 'Config file', active_lang)}:[/cyan] {project_dir / '.shipgit.yml'}")


@app.command("config-lang")
def config_lang(
    language: str = typer.Argument(..., help="Language to save: zh / en / bi"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project directory."),
    lang: str | None = typer.Option(None, "--lang", "-l", help="Output language: zh / en / bi"),
) -> None:
    """
    Set default language for current project.
    """
    project_dir = resolve_project_dir(path)
    target_language = normalize_lang(language)
    active_lang = apply_language(project_dir, lang)

    config = load_config(project_dir)
    config.language = target_language
    save_config(project_dir, config)
    set_lang(target_language)

    console.print(
        f"[green]{text('默认语言已设置为', 'Default language set to', active_lang)}:[/green] {target_language}"
    )


@app.command("remote-add")
def remote_add(
    name: str = typer.Argument(..., help="Remote name, for example github or gitee."),
    url: str = typer.Argument(..., help="Remote URL."),
    path: str | None = typer.Option(None, "--path", "-p", help="Project directory."),
    lang: str | None = typer.Option(None, "--lang", "-l", help="Language: zh / en / bi"),
) -> None:
    """
    Add or update a Git remote and save it to .shipgit.yml.
    """
    project_dir = resolve_project_dir(path)
    active_lang = apply_language(project_dir, lang)

    if not is_git_repo(project_dir):
        console.print(
            f"[yellow]{text('当前目录不是 Git 仓库，正在初始化...', 'This directory is not a Git repository. Initializing...', active_lang)}[/yellow]"
        )
        init_repo(project_dir, lang=active_lang)

    add_remote(project_dir, name, url, lang=active_lang)
    add_or_update_remote_config(project_dir, name, url)

    console.print(f"[green]{text('远程仓库已保存到 ShipGit 配置。', 'Remote saved to ShipGit config.', active_lang)}[/green]")


@app.command("remote-list")
def remote_list(
    path: str | None = typer.Argument(None, help="Project directory. Default: current directory."),
    lang: str | None = typer.Option(None, "--lang", "-l", help="Language: zh / en / bi"),
) -> None:
    """
    List Git remotes.
    """
    project_dir = resolve_project_dir(path)
    active_lang = apply_language(project_dir, lang)
    remotes = get_remotes(project_dir)

    if not remotes:
        console.print(f"[yellow]{text('尚未配置 Git 远程仓库。', 'No Git remotes configured.', active_lang)}[/yellow]")
        return

    for name, url in remotes.items():
        console.print(f"[cyan]{name}[/cyan] -> {url}")


@app.command()
def status(
    path: str | None = typer.Argument(None, help="Project directory. Default: current directory."),
    lang: str | None = typer.Option(None, "--lang", "-l", help="Language: zh / en / bi"),
) -> None:
    """
    Show changed files.
    """
    project_dir = resolve_project_dir(path)
    active_lang = apply_language(project_dir, lang)
    print_status(project_dir, lang=active_lang)


@app.command(name="publish")
def publish_cmd(
    path: str | None = typer.Option(None, "--path", "-p", help="Project directory."),
    message: str | None = typer.Option(None, "--message", "-m", help="Commit message."),
    tag: str | None = typer.Option(None, "--tag", "-t", help="Optional tag, such as v0.1.0."),
    all_remotes: bool = typer.Option(False, "--all-remotes", help="Push to all remotes."),
    branch: str | None = typer.Option(None, "--branch", "-b", help="Branch name. Default: current branch."),
    lang: str | None = typer.Option(None, "--lang", "-l", help="Language: zh / en / bi"),
) -> None:
    """
    Commit, optionally tag, and push to selected remotes.
    """
    project_dir = resolve_project_dir(path)
    active_lang = apply_language(project_dir, lang)

    if not is_git_repo(project_dir):
        create = questionary.confirm(
            text("当前目录不是 Git 仓库，是否现在初始化？", "This directory is not a Git repository. Initialize it now?", active_lang),
            default=True,
        ).ask()

        if create:
            init_repo(project_dir, lang=active_lang)
        else:
            console.print(f"[red]{text('发布已取消。', 'Publish cancelled.', active_lang)}[/red]")
            raise typer.Exit(code=1)

    if not (project_dir / ".gitignore").exists():
        create_gitignore = questionary.confirm(
            text("未找到 .gitignore，是否创建推荐模板？", ".gitignore not found. Create a recommended .gitignore?", active_lang),
            default=True,
        ).ask()

        if create_gitignore:
            ensure_gitignore(project_dir, create_if_missing=True)
            console.print(f"[green]{text('.gitignore 已创建。', '.gitignore created.', active_lang)}[/green]")

    console.print(f"[bold]{text('当前变更', 'Current changes', active_lang)}:[/bold]")
    print_status(project_dir, lang=active_lang)

    if not message:
        message = questionary.text(
            text("提交说明", "Commit message", active_lang) + ":",
            default="feat: update project",
        ).ask()

    if not message or not message.strip():
        console.print(f"[red]{text('提交说明不能为空。', 'Commit message is required.', active_lang)}[/red]")
        raise typer.Exit(code=1)

    if tag is None:
        tag = questionary.text(
            text("Tag，可选。直接回车跳过", "Tag, optional. Press Enter to skip", active_lang) + ":",
            default="",
        ).ask()

    tag = tag.strip() if tag else None

    remotes_dict = get_remotes(project_dir)

    if not remotes_dict:
        console.print(f"[yellow]{text('尚未配置 Git 远程仓库。', 'No Git remote configured.', active_lang)}[/yellow]")

        should_add = questionary.confirm(
            text("是否现在添加远程仓库？", "Do you want to add a remote now?", active_lang),
            default=True,
        ).ask()

        if should_add:
            remote_name = questionary.text(text("远程仓库名称", "Remote name", active_lang) + ":", default="github").ask()
            remote_url = questionary.text(text("远程仓库 URL", "Remote URL", active_lang) + ":").ask()

            if not remote_name or not remote_url:
                console.print(f"[red]{text('远程仓库名称和 URL 不能为空。', 'Remote name and URL are required.', active_lang)}[/red]")
                raise typer.Exit(code=1)

            add_remote(project_dir, remote_name, remote_url, lang=active_lang)
            add_or_update_remote_config(project_dir, remote_name, remote_url)
            remotes_dict = get_remotes(project_dir)
        else:
            console.print(f"[red]{text('由于没有远程仓库，发布已取消。', 'Publish cancelled because no remote exists.', active_lang)}[/red]")
            raise typer.Exit(code=1)

    available_remotes = sorted(remotes_dict.keys())

    if all_remotes:
        selected_remotes = available_remotes
    else:
        selected_remotes = questionary.checkbox(
            text("选择要推送的远程仓库", "Select remotes to push", active_lang) + ":",
            choices=available_remotes,
            default=available_remotes,
        ).ask()

    if not selected_remotes:
        console.print(f"[red]{text('没有选择远程仓库，发布已取消。', 'No remote selected. Publish cancelled.', active_lang)}[/red]")
        raise typer.Exit(code=1)

    selected_branch = branch or get_current_branch(project_dir) or "main"

    confirm = questionary.confirm(
        text(
            f"确认发布到 {', '.join(selected_remotes)} 的 {selected_branch} 分支？",
            f"Publish to {', '.join(selected_remotes)} on branch '{selected_branch}'?",
            active_lang,
        ),
        default=True,
    ).ask()

    if not confirm:
        console.print(f"[yellow]{text('发布已取消。', 'Publish cancelled.', active_lang)}[/yellow]")
        raise typer.Exit(code=0)

    publish(
        project_dir=project_dir,
        message=message.strip(),
        tag=tag,
        remotes=selected_remotes,
        branch=selected_branch,
        add_all=True,
        push_tags=True,
        lang=active_lang,
    )


if __name__ == "__main__":
    app()
