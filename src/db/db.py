from loguru import logger
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from src.utils.settings import Settings

Select.inherit_cache = True
SelectOfScalar.inherit_cache = True


class DB(BaseModel):
    settings: Settings
    _engine: AsyncEngine | None = None
    _session_make: async_sessionmaker[AsyncSession] | None = None

    @property
    def engine(self) -> AsyncEngine:
        assert self._engine is not None, "DB AsyncEngine not init"
        return self._engine

    @property
    def session_make(self) -> async_sessionmaker[AsyncSession]:
        assert (
            self._session_make is not None
        ), "DB async_sessionmaker[AsyncSession] not init"
        return self._session_make

    async def init(self) -> None:
        logger.info("DB init...")
        self._engine = create_async_engine(
            self.settings.DATABASE_URL, echo=self.settings.DEBUG, future=True
        )
        self._session_make = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info("DB init done")

    async def check(self) -> None:
        async with self.engine.connect() as con:
            await con.execute(text("SELECT 1"))
