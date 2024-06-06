"""
默认信息:

- 格式: `[%(asctime)s %(name)s] %(levelname)s: %(message)s`
- 等级: `INFO` ，根据 `settings.log_level` 配置改变
- 输出: 输出至 stdout
"""

from __future__ import annotations

import re
import sys
from re import Match
from typing import TYPE_CHECKING, Any

import loguru


if TYPE_CHECKING:
    from loguru import Logger, Record

logger: Logger = loguru.logger


LOG_LEVEL = "INFO"
LOG_SENSITIZE_KEYS = ["Cookie"]
PROJECT_NAME = "<set project name>"


def desensitize_value(value: str) -> str:
    if len(value) > 6:
        start = value[:3]
        end = value[-4:] if value.endswith("'") or value.endswith('"') else value[-3:]
        return f"{start}{'*' * 5}{end}"
    else:
        return value


def desensitize_data(message: str, keywords: list[str]) -> str:
    def header_replacer(match: Match[str]) -> str:
        key = match.group(1)
        quotes1 = match.group(2)
        value = match.group(3)
        if value and key:
            return key + quotes1 + desensitize_value(value)
        else:
            return match.group(0)

    for keyword in keywords:
        message = re.sub(
            rf"(['\"]?{keyword}['\"]?[=:]\s?)(['\"]?)(.*?['\"]?[^;,]+)",
            header_replacer,
            message,
            flags=re.IGNORECASE,
        )
    return message


def default_filter(record: Record | dict[str, Any]) -> bool:
    log_level = LOG_LEVEL
    levelno = logger.level(log_level).no if isinstance(log_level, str) else log_level
    if LOG_SENSITIZE_KEYS:
        record["message"] = desensitize_data(record["message"], LOG_SENSITIZE_KEYS)
    return int(record["level"].no) >= int(levelno)


logger.remove()

if LOG_LEVEL == "DEBUG":
    diagnose = True
    backtrace = True
    default_format: str = (
        "<g>{time:MM-DD HH:mm:ss}</g> "
        "[<lvl>{level}</lvl>] "
        "<c><u>{name}</u></c> | "
        "<c>{function}:{line}</c> | "
        "{message}"
    )
    """默认日志格式"""
else:
    diagnose = False
    backtrace = False
    default_format = (
        "<g>{time:MM-DD HH:mm:ss}</g> "
        "[<lvl>{level}</lvl>] "
        f"<c><u>{PROJECT_NAME}</u></c> | "
        "{message}"
    )
    """默认日志格式"""

logger_id = logger.add(
    sys.stdout,
    level=0,
    diagnose=diagnose,
    filter=default_filter,
    format=default_format,
    backtrace=backtrace,
)
"""默认日志处理器 id"""

__autodoc__ = {"logger_id": False}
