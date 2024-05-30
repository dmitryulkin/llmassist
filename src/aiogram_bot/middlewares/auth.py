from typing import Any
from aiogram import BaseMiddleware
from sqlalchemy.exc import NoResultFound
from sqlmodel.ext.asyncio.session import AsyncSession
from aiogram.types import TelegramObject
from collections.abc import Awaitable, Callable

from src.aiogram_bot.db.tg_user import get_user_id


class AuthMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        if not user:
            return await handler(event, data)

        session: AsyncSession = data["session"]
        try:
            await get_user_id(user.id, session)
            return await handler(event, data)
        except NoResultFound:
            # skip anautorized users silently
            return
