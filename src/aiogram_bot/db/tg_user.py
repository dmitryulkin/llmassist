from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models.user import User

__all__ = ["TgUser"]


class TgUser(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    tg_id: int

    app_user_id: int | None = Field(default=None, foreign_key="user.id")


async def get_user_id(tg_id: int, session: AsyncSession) -> int:
    stmt = (
        select(TgUser, User)
        .where(TgUser.app_user_id == User.id)
        .where(TgUser.tg_id == tg_id)
    )
    result = await session.exec(stmt)
    _, user = result.one()
    return user.id
