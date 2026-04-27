from __future__ import annotations

import subprocess
from pathlib import Path
from dataclasses import dataclass


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


class CommandError(RuntimeError):
    def __init__(self, result: CommandResult):
        self.result = result
        command_text = " ".join(result.command)
        message = (
            f"Command failed: {command_text}\n"
            f"Return code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
        super().__init__(message)


def run_command(
    project_dir: Path,
    command: list[str],
    check: bool = False,
) -> CommandResult:
    completed = subprocess.run(
        command,
        cwd=str(project_dir),
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
    )

    result = CommandResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )

    if check and not result.ok:
        raise CommandError(result)

    return result


def run_git(
    project_dir: Path,
    args: list[str],
    check: bool = False,
) -> CommandResult:
    return run_command(project_dir, ["git", *args], check=check)
