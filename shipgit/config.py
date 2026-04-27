from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass, field
import yaml

from shipgit.i18n import normalize_lang


CONFIG_FILE_NAME = ".shipgit.yml"


@dataclass
class RemoteConfig:
    name: str
    url: str
    enabled: bool = True


@dataclass
class ShipGitConfig:
    project_name: str = ""
    default_branch: str = "main"
    push_tags: bool = True
    require_gitignore: bool = True
    language: str = "zh"
    remotes: list[RemoteConfig] = field(default_factory=list)


def get_config_path(project_dir: Path) -> Path:
    return project_dir / CONFIG_FILE_NAME


def load_config(project_dir: Path) -> ShipGitConfig:
    path = get_config_path(project_dir)

    if not path.exists():
        return ShipGitConfig(project_name=project_dir.name)

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    project_data = data.get("project", {})
    publish_data = data.get("publish", {})
    ui_data = data.get("ui", {})
    remote_data = data.get("remotes", [])

    remotes = [
        RemoteConfig(
            name=item.get("name", ""),
            url=item.get("url", ""),
            enabled=bool(item.get("enabled", True)),
        )
        for item in remote_data
        if item.get("name") and item.get("url")
    ]

    return ShipGitConfig(
        project_name=project_data.get("name", project_dir.name),
        default_branch=project_data.get("defaultBranch", "main"),
        push_tags=bool(publish_data.get("pushTags", True)),
        require_gitignore=bool(publish_data.get("requireGitignore", True)),
        language=normalize_lang(ui_data.get("language", "zh")),
        remotes=remotes,
    )


def save_config(project_dir: Path, config: ShipGitConfig) -> None:
    path = get_config_path(project_dir)

    data = {
        "project": {
            "name": config.project_name,
            "defaultBranch": config.default_branch,
        },
        "ui": {
            "language": normalize_lang(config.language),
        },
        "remotes": [
            {
                "name": remote.name,
                "url": remote.url,
                "enabled": remote.enabled,
            }
            for remote in config.remotes
        ],
        "publish": {
            "pushTags": config.push_tags,
            "requireGitignore": config.require_gitignore,
        },
    }

    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def add_or_update_remote_config(
    project_dir: Path,
    name: str,
    url: str,
    enabled: bool = True,
) -> ShipGitConfig:
    config = load_config(project_dir)

    for remote in config.remotes:
        if remote.name == name:
            remote.url = url
            remote.enabled = enabled
            save_config(project_dir, config)
            return config

    config.remotes.append(RemoteConfig(name=name, url=url, enabled=enabled))
    save_config(project_dir, config)
    return config
