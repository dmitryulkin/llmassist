import pytest

from tests.mocks import SettingsMock


def test_default_settings():
    settings = SettingsMock()
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.LOG_TO_FILE is False
    assert settings.TOR_SOCKS5_PORT is None


def test_loglevel_invalid():
    with pytest.raises(ValueError):
        SettingsMock(LOG_LEVEL="dummy")  # type: ignore


@pytest.mark.parametrize("port", [-1, 0])
def test_tor_port(port: int):
    with pytest.raises(Exception):
        SettingsMock(TOR_SOCKS5_PORT=port)
