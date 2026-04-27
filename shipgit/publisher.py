from __future__ import annotations

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from shipgit.git_runner import run_git
from shipgit.checks import get_git_status, get_current_branch, get_remotes
from shipgit.i18n import text, cell_text, title_text


console = Console()


def explain_git_status(code: str, lang: str = "zh") -> str:
    code = code.strip()

    mapping = {
        "??": ("未跟踪", "Untracked"),
        "A": ("新增", "Added"),
        "M": ("已修改", "Modified"),
        "D": ("已删除", "Deleted"),
        "R": ("重命名", "Renamed"),
        "C": ("复制", "Copied"),
        "U": ("冲突", "Unmerged"),
        "T": ("类型变更", "Type changed"),
        "!!": ("已忽略", "Ignored"),
    }

    if code in mapping:
        zh, en = mapping[code]
        return cell_text(zh, en, lang)

    if len(code) == 2:
        index_status = code[0]
        worktree_status = code[1]

        parts: list[str] = []

        if index_status != " ":
            parts.append(
                cell_text("暂存区", "Index", lang)
                + ": "
                + explain_git_status(index_status, lang)
            )

        if worktree_status != " ":
            parts.append(
                cell_text("工作区", "Worktree", lang)
                + ": "
                + explain_git_status(worktree_status, lang)
            )

        if parts:
            return "\n".join(parts) if lang == "bi" else " / ".join(parts)

    return cell_text("未知状态", "Unknown status", lang)


def init_repo(project_dir: Path, lang: str = "zh") -> None:
    if (project_dir / ".git").exists():
        console.print(f"[green]{text('Git 仓库已存在。', 'Git repository already exists.', lang)}[/green]")
        return

    result = run_git(project_dir, ["init"])
    if result.ok:
        console.print(f"[green]{text('Git 仓库初始化成功。', 'Git repository initialized.', lang)}[/green]")
    else:
        console.print(f"[red]{text('Git 仓库初始化失败。', 'Failed to initialize Git repository.', lang)}[/red]")
        console.print(result.stderr)


def add_remote(project_dir: Path, name: str, url: str, lang: str = "zh") -> None:
    remotes = get_remotes(project_dir)

    if name in remotes:
        console.print(
            f"[yellow]{text('远程仓库已存在，正在更新 URL：', 'Remote already exists. Updating URL:', lang)} {name}[/yellow]"
        )
        result = run_git(project_dir, ["remote", "set-url", name, url])
    else:
        result = run_git(project_dir, ["remote", "add", name, url])

    if result.ok:
        console.print(f"[green]{text('远程仓库配置成功：', 'Remote configured:', lang)}[/green] {name} -> {url}")
    else:
        console.print(f"[red]{text('远程仓库配置失败：', 'Failed to configure remote:', lang)} {name}[/red]")
        console.print(result.stderr)


def print_status(project_dir: Path, lang: str = "zh") -> None:
    status = get_git_status(project_dir)

    if not status:
        console.print(
            f"[green]{text('工作区干净，没有待提交变更。', 'Working tree clean. No changes to commit.', lang)}[/green]"
        )
        return

    if lang == "zh":
        code_title = "状态码"
        meaning_title = "状态说明"
        file_title = "文件"
    elif lang == "en":
        code_title = "Code"
        meaning_title = "Meaning"
        file_title = "File"
    else:
        code_title = "Code"
        meaning_title = cell_text("状态说明", "Meaning", lang)
        file_title = cell_text("文件", "File", lang)

    table = Table(
        title=title_text("变更文件", "Changed Files", lang),
        box=box.SQUARE,
        show_lines=True,
        expand=False,
    )

    table.add_column("No.", style="magenta", width=4, no_wrap=True, justify="right")
    table.add_column(code_title, style="cyan", width=8, no_wrap=True)
    table.add_column(meaning_title, style="green", min_width=14, overflow="fold")
    table.add_column(file_title, min_width=26, overflow="fold")

    for index, line in enumerate(status, start=1):
        raw_code = line[:2]
        code = raw_code.strip()
        file_path = line[3:] if len(line) > 3 else line

        table.add_row(
            str(index),
            code or "-",
            explain_git_status(code, lang),
            file_path,
        )

    console.print(table)


def create_commit(project_dir: Path, message: str, add_all: bool = True, lang: str = "zh") -> bool:
    add_args = ["add", "."] if add_all else ["add", "-u"]
    add_result = run_git(project_dir, add_args)

    if not add_result.ok:
        console.print(f"[red]{text('git add 执行失败。', 'git add failed.', lang)}[/red]")
        console.print(add_result.stderr)
        return False

    staged_result = run_git(project_dir, ["diff", "--cached", "--name-only"])
    if not staged_result.stdout:
        console.print(f"[yellow]{text('没有暂存变更，跳过 commit。', 'No staged changes. Commit skipped.', lang)}[/yellow]")
        return False

    commit_result = run_git(project_dir, ["commit", "-m", message])

    if commit_result.ok:
        console.print(f"[green]{text('Commit 创建成功。', 'Commit created successfully.', lang)}[/green]")
        return True

    console.print(f"[red]{text('git commit 执行失败。', 'git commit failed.', lang)}[/red]")
    console.print(commit_result.stderr)
    return False


def create_tag(project_dir: Path, tag: str, lang: str = "zh") -> bool:
    if not tag:
        return False

    existing = run_git(project_dir, ["tag", "--list", tag])
    if existing.ok and existing.stdout.strip() == tag:
        console.print(f"[yellow]{text('Tag 已在本地存在，已跳过：', 'Tag already exists locally. Skipped:', lang)} {tag}[/yellow]")
        return False

    result = run_git(project_dir, ["tag", tag])

    if result.ok:
        console.print(f"[green]{text('Tag 创建成功：', 'Tag created:', lang)}[/green] {tag}")
        return True

    console.print(f"[red]{text('Tag 创建失败：', 'Failed to create tag:', lang)} {tag}[/red]")
    console.print(result.stderr)
    return False


def push_branch(project_dir: Path, remote: str, branch: str, lang: str = "zh") -> bool:
    console.print(f"[cyan]{text('正在推送分支', 'Pushing branch', lang)} '{branch}' -> '{remote}'...[/cyan]")
    result = run_git(project_dir, ["push", "-u", remote, branch])

    if result.ok:
        console.print(f"[green]{text('分支推送成功', 'Pushed branch successfully', lang)}: {remote}/{branch}[/green]")
        return True

    console.print(f"[red]{text('分支推送失败', 'Failed to push branch', lang)}: {remote}/{branch}[/red]")
    console.print(result.stderr)
    return False


def push_tag(project_dir: Path, remote: str, tag: str, lang: str = "zh") -> bool:
    if not tag:
        return False

    console.print(f"[cyan]{text('正在推送 Tag', 'Pushing tag', lang)} '{tag}' -> '{remote}'...[/cyan]")
    result = run_git(project_dir, ["push", remote, tag])

    if result.ok:
        console.print(f"[green]{text('Tag 推送成功', 'Pushed tag successfully', lang)}: {remote}/{tag}[/green]")
        return True

    console.print(f"[red]{text('Tag 推送失败', 'Failed to push tag', lang)}: {remote}/{tag}[/red]")
    console.print(result.stderr)
    return False


def publish(
    project_dir: Path,
    message: str,
    tag: str | None,
    remotes: list[str],
    branch: str | None = None,
    add_all: bool = True,
    push_tags: bool = True,
    lang: str = "zh",
) -> None:
    branch = branch or get_current_branch(project_dir)

    console.print(
        Panel.fit(
            f"[bold]{text('分支', 'Branch', lang)}:[/bold] {branch}\n"
            f"[bold]{text('提交说明', 'Commit', lang)}:[/bold] {message}\n"
            f"[bold]Tag:[/bold] {tag or '-'}\n"
            f"[bold]{text('远程仓库', 'Remotes', lang)}:[/bold] {', '.join(remotes)}",
            title=title_text("ShipGit 发布计划", "ShipGit Publish Plan", lang),
        )
    )

    committed = create_commit(project_dir, message, add_all=add_all, lang=lang)
    tag_created = False

    if tag:
        tag_created = create_tag(project_dir, tag, lang=lang)

    if not committed and not tag_created:
        console.print(
            f"[yellow]{text('没有创建 commit 或 tag，但仍会尝试推送。', 'No commit or tag created. Push will still be attempted.', lang)}[/yellow]"
        )

    success_count = 0
    fail_count = 0

    for remote in remotes:
        ok = push_branch(project_dir, remote, branch, lang=lang)
        success_count += 1 if ok else 0
        fail_count += 0 if ok else 1

        if tag and push_tags:
            tag_ok = push_tag(project_dir, remote, tag, lang=lang)
            success_count += 1 if tag_ok else 0
            fail_count += 0 if tag_ok else 1

    console.print(
        Panel.fit(
            f"[green]{text('成功', 'Success', lang)}:[/green] {success_count}\n"
            f"[red]{text('失败', 'Failed', lang)}:[/red] {fail_count}",
            title=title_text("ShipGit 发布结果", "ShipGit Publish Result", lang),
        )
    )
