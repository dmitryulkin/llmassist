from types import NoneType

import pytest
from loguru import logger
from pytest import CaptureFixture, LogCaptureFixture

from src.context import ctx


@pytest.mark.parametrize(
    "patch_settings", [{"LOG_LEVEL": "INFO"}], indirect=True
)
def test_console_only_logging(
    patch_settings: NoneType, caplog: LogCaptureFixture
):
    ctx.init()
    caplog.set_level(ctx.settings.LOG_LEVEL)
    logger.info("TEST INFO")
    logger.debug("TEST DEBUG")
    assert "TEST DEBUG" not in caplog.text and "TEST INFO" in caplog.text
    # here should be no log file
    assert not ctx.settings.LOG_FILE.is_file()


@pytest.mark.parametrize(
    "patch_settings, result",
    [
        (
            {
                "LOG_LEVEL": "WARNING",
                "LOG_TO_FILE": True,
                "LOG_FILE_LEVEL": "INFO",
            },
            {
                "CONSOLE_INFO": False,
                "CONSOLE_WARN": True,
                "FILE_INFO": True,
                "FILE_WARN": True,
            },
        ),
        (
            {
                "LOG_LEVEL": "INFO",
                "LOG_TO_FILE": True,
                "LOG_FILE_LEVEL": "WARNING",
            },
            {
                "CONSOLE_INFO": True,
                "CONSOLE_WARN": True,
                "FILE_INFO": False,
                "FILE_WARN": True,
            },
        ),
    ],
    indirect=["patch_settings"],
)
def test_console_and_file_logging(
    patch_settings: NoneType,
    result: dict[str, bool],
    capsys: CaptureFixture[str],
):
    ctx.init()
    logger.info("TEST INFO")
    logger.warning("TEST WARNING")
    out: str = capsys.readouterr().out
    assert ("TEST INFO" in out) is result["CONSOLE_INFO"]
    assert ("TEST WARNING" in out) is result["CONSOLE_WARN"]
    # check file logging
    with open(ctx.settings.LOG_FILE, "r") as log_file:
        read_log = log_file.read()
        assert ("TEST INFO" in read_log) is result["FILE_INFO"]
        assert ("TEST WARNING" in read_log) is result["FILE_WARN"]
