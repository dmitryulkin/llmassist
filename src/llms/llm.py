from collections.abc import AsyncIterator

from loguru import logger
from pydantic import BaseModel

from src.db.services.settings import LLMSettings
from src.exceptions import LLMError
from src.llms.g4f_service import GPT4FreeLLMService
from src.llms.llm_service import LLMChat, LLMService
from src.utils.settings import Settings


class LLM(BaseModel):
    settings: Settings
    services: dict[str, LLMService] = {}

    def init(self):
        logger.info("LLM init...")
        self.services[GPT4FreeLLMService.get_name()] = GPT4FreeLLMService()
        logger.info("LLM init done")

    async def chat_completion(
        self, chat: LLMChat, llm_settings: LLMSettings
    ) -> str | AsyncIterator[str]:
        if (
            GPT4FreeLLMService.get_name() == llm_settings.service
            and llm_settings.provider
            and llm_settings.model
        ):
            config = {
                "provider": llm_settings.provider,
                "model": llm_settings.model,
            }
            return await self.services[
                GPT4FreeLLMService.get_name()
            ].chat_completion(chat, config)
        raise LLMError(
            "LLM Chat Completion could not be created: check LLM settings"
        )
