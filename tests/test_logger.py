import logging

import pytest

from src.utils.context import ctx
from src.utils.loggers import get_logger


@pytest.mark.parametrize(
    "patch_settings", [{"LOG_LEVEL": logging.INFO}], indirect=True
)
def test_console_only_logging(patch_settings, caplog):
    logger = get_logger(__name__)
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
                "LOG_LEVEL": logging.WARNING,
                "LOG_TO_FILE": True,
                "LOG_FILE_LEVEL": logging.INFO,
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
                "LOG_LEVEL": logging.INFO,
                "LOG_TO_FILE": True,
                "LOG_FILE_LEVEL": logging.WARNING,
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
def test_console_and_file_logging(patch_settings, result, capsys):
    logger = get_logger(__name__)
    logger.info("TEST INFO")
    logger.warning("TEST WARNING")
    _, err = capsys.readouterr()
    assert ("TEST INFO" in err) is result["CONSOLE_INFO"]
    assert ("TEST WARNING" in err) is result["CONSOLE_WARN"]
    # check file logging
    with open(ctx.settings.LOG_FILE, "r") as log_file:
        read_log = log_file.read()
        assert ("TEST INFO" in read_log) is result["FILE_INFO"]
        assert ("TEST WARNING" in read_log) is result["FILE_WARN"]
