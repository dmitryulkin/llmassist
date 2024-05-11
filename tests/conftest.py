from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger
from pytest import FixtureRequest, MonkeyPatch

from src.services import srv
from tests.mocks import SettingsMock


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    """override caplog to use loguru"""
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        # Set to 'True' if your test is spawning child processes.
        enqueue=False,
    )
    yield caplog
    logger.remove(handler_id)


@pytest.fixture
def patch_settings(
    tmp_path: Path, request: FixtureRequest, monkeypatch: MonkeyPatch
) -> None:
    """patch ctx.settings with value from request param
    - log to tmp_path
    """
    settings = SettingsMock()
    settings.LOG_FILE = tmp_path / settings.LOG_FILE

    # Patch the settings with the param vars
    stgs_vars = getattr(request, "param", {})
    for key, val in stgs_vars.items():
        # check key settings exists
        if not hasattr(settings, key):
            raise ValueError(f"Unknown setting: {key}")
        # check settings val type is appropriate
        expected_type = getattr(settings, key).__class__
        if not isinstance(val, expected_type):
            raise ValueError(
                f"Invalid type for {key}: {val.__class__} instead "
                "of {expected_type}"
            )
        # set key
        setattr(settings, key, val)

    monkeypatch.setattr(srv, "settings", settings)
