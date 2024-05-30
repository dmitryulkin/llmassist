from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache
from aiogram.types import TelegramObject

RATE_LIMIT: float = 1


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=RATE_LIMIT)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        # filters only Messages
        if not isinstance(event, Message):
            return await handler(event, data)

        if event.chat.id in self.cache:
            return None
        self.cache[event.chat.id] = None
        return await handler(event, data)
