from types import NoneType

import pytest

from src.services import srv


@pytest.mark.parametrize(
    "patch_settings",
    [{"SQLITE_DB_FILE": ""}],
    indirect=True,
)
async def test_sqlite_inmemory_init(patch_settings: NoneType):
    await srv.init_db()
