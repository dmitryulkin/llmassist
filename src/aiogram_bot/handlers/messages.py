from time import time

import g4f.models
from aiogram import F, Router, types
from g4f.client import AsyncClient
from g4f.Provider import Bing
from g4f.providers.types import ProviderType
from g4f.typing import Messages

from src.exceptions import CustomError
from src.services import srv

router = Router(name="messages")


async def llm_completion(
    chat_messages: Messages, provider: ProviderType, stream: bool = False
):
    proxy_url = await srv.proxy.get_proxy_url()
    client = AsyncClient(
        provider=provider,
        # proxies={"http": proxy_url, "https": proxy_url},
    )
    completion = client.chat.completions.create(
        model=g4f.models.default.name,
        messages=chat_messages,
        stream=stream,
        proxy=proxy_url,
    )
    return completion


@router.message(F.text)
async def message_handler(message: types.Message) -> None:
    if message.text is None:
        raise CustomError("Message with None text received")

    messages: Messages = [
        {
            "role": "system",
            "content": "Привет! Ты - ИИ-помощник для бизнеса в Telegram."
            " Отвечай на вопросы пользователей",
        },
        {"role": "user", "content": message.text},
    ]
    provider = Bing
    stream = True
    completion = await llm_completion(messages, provider, stream)
    if stream:
        answer_msg = await message.answer("...")
        responce: str = ""
        sent_time: float = time()
        async for chunk in completion:
            if chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                if isinstance(delta, str):
                    responce += delta
                else:
                    continue
            if int((cur_time := time()) - sent_time) > 2:
                sent_time = cur_time
                await answer_msg.edit_text(responce)
        await answer_msg.edit_text(responce)
    else:
        responce = await completion
        await message.answer(responce.choices[0].message.content)
