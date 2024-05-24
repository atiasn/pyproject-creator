"""
默认信息:

- 格式: `[%(asctime)s %(name)s] %(levelname)s: %(message)s`
- 等级: `INFO` ，根据 `settings.log_level` 配置改变
- 输出: 输出至 stdout
"""

import re
import sys
import inspect
import logging
from typing import TYPE_CHECKING

import loguru

if TYPE_CHECKING:
    from loguru import Logger, Record

logger: "Logger" = loguru.logger


# default_handler = logging.StreamHandler(sys.stdout)
# default_handler.setFormatter(
#     logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s"))
# logger.addHandler(default_handler)


class LoguruHandler(logging.Handler):  # pragma: no cover
    """logging 与 loguru 之间的桥梁，将 logging 的日志转发到 loguru。"""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def desensitize_cookie_values(cookie):
    # 匹配 key=value 对，考虑结尾可能没有分号的情况
    def replacer(match):
        key = match.group(1)
        value = match.group(2)
        if len(value) > 6:
            start = value[:3]
            end = value[-3:]
            return f"{key}={start}{'*' * 5}{end}"
        else:
            return f"{key}={value}"

    return re.sub(r"(\w+)=([^;]+)", replacer, cookie)


def desensitize_cookie_data(message):
    # 用于匹配整个 'Cookie: ...' 头部，并只对该部分进行脱敏
    pattern = r"'Cookie': '([^']+)'"

    def header_replacer(match):
        cookie = match.group(1)
        return f"'Cookie': '{desensitize_cookie_values(cookie)}'"

    return re.sub(pattern, header_replacer, message)


def default_filter(record: "Record"):
    log_level = settings.LOG_LEVEL
    levelno = logger.level(log_level).no if isinstance(log_level, str) else log_level
    if settings.LOG_SENSITIZE:
        record["message"] = desensitize_cookie_data(record["message"])
    return record["level"].no >= levelno


logger.remove()

if settings.LOG_LEVEL == "DEBUG":
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
    default_format: str = (
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
