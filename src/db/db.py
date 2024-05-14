from dataclasses import dataclass

from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from src.services import srv

Select.inherit_cache = True
SelectOfScalar.inherit_cache = True


@dataclass
class DB:
    engine = None
    make_session = None

    def __init__(self) -> None:
        logger.info("DB init...")
        self.engine = create_async_engine(
            srv.settings.DATABASE_URL, echo=srv.settings.DEBUG, future=True
        )
        self.make_session = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info("DB init done")

    async def check(self) -> None:
        async with self.engine.connect() as con:
            await con.execute(text("SELECT 1"))
