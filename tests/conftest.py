import copy
from pathlib import Path
from types import NoneType

import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger
from pytest import FixtureRequest

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
def save_loguru_state():
    """loguru logger is the global object and there is no convinient method
    to manage handlers when settings of logging changed from test to test.
    This fixture saves handlers before some changes of logger settings and
    restores them on exit"""
    _core = getattr(logger, "_core")
    handlers = copy.copy(getattr(_core, "handlers"))
    yield
    setattr(_core, "handlers", handlers)


@pytest.fixture
def patch_settings(
    save_loguru_state: NoneType, tmp_path: Path, request: FixtureRequest
):
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
        # set key
        setattr(settings, key, val)
    saved = srv.settings
    srv.settings = settings
    yield
    srv.settings = saved
