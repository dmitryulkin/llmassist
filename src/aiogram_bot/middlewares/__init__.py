from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    # outer middlewares
    from .auth import AuthMiddleware
    from .db import DatabaseMiddleware

    # order matters
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.update.outer_middleware(AuthMiddleware())

    # middlewares
    dp.message.middleware(ChatActionMiddleware())
