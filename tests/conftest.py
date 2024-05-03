from pathlib import Path

import pytest
from pytest import FixtureRequest, MonkeyPatch

from src.utils.context import ctx
from tests.mocks import SettingsMock


@pytest.fixture
def patch_settings(
    tmp_path: Path, request: FixtureRequest, monkeypatch: MonkeyPatch
) -> None:
    settings = SettingsMock()
    settings.LOG_FILE = tmp_path / ctx.settings.LOG_FILE

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

    monkeypatch.setattr(ctx, "settings", settings)
