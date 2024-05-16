import pytest

from src.services import srv
from src.utils.settings import Settings


@pytest.mark.parametrize(
    "settings",
    [{"SQLITE_DB_FILE": ""}],
    indirect=True,
)
async def test_sqlite_inmemory_init(settings: Settings):
    await srv.init_db(settings)
