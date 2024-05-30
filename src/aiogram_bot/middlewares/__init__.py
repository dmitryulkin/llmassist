from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    # outer middlewares
    from .db import DatabaseMiddleware

    dp.update.outer_middleware(DatabaseMiddleware())

    # middlewares
    dp.message.middleware(ChatActionMiddleware())
