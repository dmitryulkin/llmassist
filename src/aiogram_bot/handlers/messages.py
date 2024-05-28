from collections.abc import AsyncIterator
from time import time

from aiogram import F, Router
from aiogram.types import Message
from sqlmodel.ext.asyncio.session import AsyncSession

from src.aiogram_bot.db.tg_user import get_user_id
from src.db.services.settings import get_user_llm_settings
from src.services import srv

router = Router(name="messages")


@router.message(F.text)
async def message_handler(message: Message, session: AsyncSession) -> None:
    if not message.text:
        return

    app_user_id = await get_user_id(message.from_user.id, session)
    llm_settings = await get_user_llm_settings(app_user_id, session)

    messages = [
        {
            "role": "system",
            "content": "Привет! Ты - ИИ-помощник для бизнеса в Telegram."
            " Отвечай на вопросы пользователей",
        },
        {"role": "user", "content": message.text},
    ]

    completion = await srv.llm.chat_completion(messages, llm_settings)

    if type(completion) is str:
        await message.answer(completion)
    elif isinstance(completion, AsyncIterator):
        answer_msg = await message.answer("...")
        responce: str = ""
        sent_time: float = time()
        async for chunk in completion:
            responce += chunk
            if int((cur_time := time()) - sent_time) > 2:
                sent_time = cur_time
                await answer_msg.edit_text(responce)
        await answer_msg.edit_text(responce)
