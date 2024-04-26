import logging

import pytest

from tests.conftest import TestSettings


def test_default_settings():
    settings = TestSettings()
    assert settings.LOG_LEVEL == logging.DEBUG
    assert settings.LOG_TO_FILE is False
    assert settings.USE_TOR is False
    assert settings.TOR_SOCKS5_PORT is None


@pytest.mark.parametrize(
    "level_str, level_int",
    [
        ("debug", logging.DEBUG),
        ("info", logging.INFO),
        ("warn", logging.WARNING),
        ("warning", logging.WARNING),
        ("error", logging.ERROR),
    ],
)
def test_loglevel_valid(level_str, level_int):
    settings = TestSettings(LOG_LEVEL=level_str)
    assert settings.LOG_LEVEL == level_int


def test_loglevel_invalid():
    with pytest.raises(ValueError):
        TestSettings(LOG_LEVEL="dummy")


@pytest.mark.parametrize("port", [None, -1, 0])
def test_tor_port(port):
    with pytest.raises(Exception):
        TestSettings(USE_TOR=True, TOR_SOCKS5_PORT=port)
