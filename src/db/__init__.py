from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from src.services import srv

Select.inherit_cache = True
SelectOfScalar.inherit_cache = True

async_engine = create_async_engine(
    srv.settings.DATABASE_URL, echo=srv.settings.DEBUG, future=True
)

make_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
