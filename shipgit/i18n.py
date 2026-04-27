from __future__ import annotations

from dataclasses import dataclass


SUPPORTED_LANGS = {"zh", "en", "bi"}


@dataclass
class RuntimeContext:
    lang: str = "zh"


ctx = RuntimeContext()


def normalize_lang(lang: str | None) -> str:
    value = (lang or "zh").lower().strip()
    if value not in SUPPORTED_LANGS:
        return "zh"
    return value


def set_lang(lang: str | None) -> None:
    ctx.lang = normalize_lang(lang)


def get_lang() -> str:
    return ctx.lang


def text(zh: str, en: str, lang: str | None = None) -> str:
    """
    普通文本：用于命令提示、交互问题、日志说明。

    双语模式下使用横向显示：
        中文 / English

    这样可以避免 questionary 交互提示里出现不自然的换行。
    """
    active_lang = normalize_lang(lang or ctx.lang)

    if active_lang == "en":
        return en

    if active_lang == "bi":
        return f"{zh} / {en}"

    return zh


def cell_text(zh: str, en: str, lang: str | None = None) -> str:
    """
    表格单元格文本：用于 Rich Table 的表头和内容。

    双语模式下使用纵向显示：
        中文
        English

    这样可以避免表格横向过宽导致标题被截断，例如：
        状态 / Stat...
    """
    active_lang = normalize_lang(lang or ctx.lang)

    if active_lang == "en":
        return en

    if active_lang == "bi":
        return f"{zh}\n{en}"

    return zh


def title_text(zh: str, en: str, lang: str | None = None) -> str:
    """
    标题文本：用于表格标题、Panel 标题。

    标题通常空间较大，双语模式可以横向显示，视觉上更自然。
    """
    return text(zh, en, lang)


def status_text(status_key: str, lang: str | None = None) -> str:
    mapping = {
        "ok": ("正常", "OK"),
        "missing": ("缺失", "Missing"),
        "changed": ("有变更", "Changed"),
        "clean": ("干净", "Clean"),
        "warning": ("警告", "Warning"),
        "unknown": ("未知", "Unknown"),
        "cancelled": ("已取消", "Cancelled"),
        "failed": ("失败", "Failed"),
        "success": ("成功", "Success"),
    }

    zh, en = mapping.get(status_key, (status_key, status_key))
    return cell_text(zh, en, lang)
