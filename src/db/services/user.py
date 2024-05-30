from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models.user import User
from src.exceptions import DBError


async def get_user(
    id: int,
    session: AsyncSession,
) -> User:
    user = await session.get(User, id)
    if user is None:
        raise DBError(f"There is no app user in DB with {id=}")
    else:
        return user
