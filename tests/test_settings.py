import pytest
from loguru import logger
from pytest import CaptureFixture, LogCaptureFixture

from src.services import srv
from src.utils.settings import Settings
from tests.mocks import SettingsMock


def test_default_settings() -> None:
    settings = SettingsMock()
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.LOG_TO_FILE is False
    assert settings.TOR_SOCKS5_PORT is None


def test_loglevel_invalid() -> None:
    with pytest.raises(ValueError):
        SettingsMock(LOG_LEVEL="dummy")  # type: ignore


@pytest.mark.parametrize("port", [-1, 0])
def test_invalid_tor_port(port: int) -> None:
    with pytest.raises(Exception):
        SettingsMock(TOR_SOCKS5_PORT=port)


@pytest.mark.parametrize("SQLITE_DB_FILE", ["not_exist.db"])
def test_invalid_sqlite_dbfile(SQLITE_DB_FILE: str) -> None:
    with pytest.raises(ValueError):
        SettingsMock(SQLITE_DB_FILE=SQLITE_DB_FILE)


async def test_invalid_db_settings() -> None:
    settings = SettingsMock()
    with pytest.raises(ValueError):
        settings.DATABASE_URL


@pytest.mark.parametrize("settings", [{"LOG_LEVEL": "INFO"}], indirect=True)
def test_console_only_logging_settings(
    settings: Settings, caplog: LogCaptureFixture
):
    caplog.set_level(settings.LOG_LEVEL)

    srv.init_loggers(settings)
    logger.info("TEST INFO")
    logger.debug("TEST DEBUG")
    assert "TEST DEBUG" not in caplog.text and "TEST INFO" in caplog.text
    # here should be no log file
    assert not settings.LOG_FILE.is_file()


@pytest.mark.parametrize(
    "settings, result",
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
    indirect=["settings"],
)
def test_console_and_file_logging_settings(
    settings: Settings,
    result: dict[str, bool],
    capsys: CaptureFixture[str],
):
    srv.init_loggers(settings)

    logger.info("TEST INFO")
    logger.warning("TEST WARNING")
    out: str = capsys.readouterr().out
    assert ("TEST INFO" in out) is result["CONSOLE_INFO"]
    assert ("TEST WARNING" in out) is result["CONSOLE_WARN"]
    # check file logging
    with open(settings.LOG_FILE, "r") as log_file:
        read_log = log_file.read()
        assert ("TEST INFO" in read_log) is result["FILE_INFO"]
        assert ("TEST WARNING" in read_log) is result["FILE_WARN"]
