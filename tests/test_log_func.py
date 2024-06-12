from __future__ import annotations

from collections.abc import Iterator

import pytest
from _pytest.logging import LogCaptureFixture

from pyproject_creator.template.logs._default import (
    logger,
    default_filter,
    desensitize_data,
    desensitize_value,
)


@pytest.fixture
def caplog(caplog: LogCaptureFixture) -> Iterator[LogCaptureFixture]:
    """Emitting logs from loguru's logger.log means that they will not show up in
    caplog which only works with Python's standard logging. This adds the same
    LogCaptureHandler being used by caplog to hook into loguru.

    Args:
        caplog (LogCaptureFixture): caplog fixture

    Yields:
        LogCaptureFixture
    """

    def filter_(record):  # type: ignore
        return record["level"].no >= caplog.handler.level

    handler_id = logger.add(caplog.handler, level=0, format="{message}", filter=filter_)
    yield caplog
    logger.remove(handler_id)


def test_desensitize_value():  # type: ignore
    assert desensitize_value("1234567890") == "123*****890"
    assert desensitize_value("12") == "12"
    assert desensitize_value("123456") == "123456"


def test_desensitize_data():  # type: ignore
    message = "'key1': 1234567890; 'key2': 'xxxxaaabcdefg'; 'key3': 'dddddddasd12345'"
    expected = "'key1': 123*****890; 'key2': 'xxx*****efg'; 'key3': 'ddd*****345'"
    assert desensitize_data(message, ["key1", "key2", "key3"]) == expected

    message = '"key1": 1234567890; "key2": "xxxxaaabcdefg"; "key3": "dddddddasd12345"'
    expected = '"key1": 123*****890; "key2": "xxx*****efg"; "key3": "ddd*****345"'
    assert desensitize_data(message, ["key1", "key2", "key3"]) == expected

    message = (
        "'Authorization': 'Bearer token1234567890', 'key1': 1234567890, 'key2': 'xxxxaaabcdefg'"
    )
    expected = (
        "'Authorization': 'Bearer token1234567890', 'key1': 123*****890, 'key2': 'xxx*****efg'"
    )
    assert desensitize_data(message, ["key1", "key2"]) == expected


def test_log_level(caplog):  # type: ignore
    # 设置记录器捕获日志
    with caplog.at_level("DEBUG"):
        logger.debug("This is a debug message")
    assert "This is a debug message" in caplog.text, "Debug message should be logged"
    assert "DEBUG" in caplog.text, "Debug message should be contains '[DEBUG]'"


def test_log_format(caplog):  # type: ignore
    logger.info("Testing format")
    logger.error("Testing error info")
    assert "Testing format" in caplog.text, "Log should contain the message"
    # Optionally check the formatting details
    assert "INFO" in caplog.text, "Log should include timestamp"
    assert "ERROR" in caplog.text, "Log should include timestamp"


def test_default_filter():  # type: ignore
    record = {"message": "Sensitive data: 'password': '123456';", "level": logger.level("INFO")}
    assert default_filter(record) is True, "Filter should pass INFO level logs"


if __name__ == "__main__":
    pytest.main()
