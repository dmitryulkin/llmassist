from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from g4f.client import AsyncClient
from g4f.Provider import ProviderType, __map__, __providers__
from g4f.providers.base_provider import AbstractProvider, ProviderModelMixin
from loguru import logger
from pydantic import BaseModel

from src.db.services.settings import LLMSettings
from src.exceptions import LLMError
from src.utils.settings import Settings

type LLMChat = list[dict[str, str]]


class LLMService(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass

    @abstractmethod
    def get_providers(self) -> list[str]:
        """
        Returns a list of all working providers.
        """
        pass

    @abstractmethod
    def get_provider_models(self, provider_name: str) -> list[str]:
        """
        Returns a list of all working models for provider.
        """
        pass

    @abstractmethod
    async def chat_completion(
        self, chat: LLMChat, config: dict[str, str]
    ) -> str | AsyncIterator[str]:
        """
        Returns LLM answer as str or AsyncIterator[str] if stream is available
        """
        pass


class GPT4FreeLLMService(LLMService):
    @classmethod
    def get_name(cls) -> str:
        return "GPT4Free"

    def get_providers(self) -> list[str]:
        return [
            provider.__name__
            for provider in __providers__
            if GPT4FreeLLMService.is_appropriate(provider)
        ]

    def get_provider_models(self, provider_name: str) -> list[str]:
        provider: ProviderType = __map__[provider_name]
        if isinstance(provider, type) and issubclass(
            provider, ProviderModelMixin
        ):
            return [model for model in provider.get_models()]
        else:
            return [
                *(["gpt-4"] if provider.supports_gpt_4 else []),
                *(["gpt-3.5-turbo"] if provider.supports_gpt_35_turbo else []),
            ]

    async def chat_completion(
        self, chat: LLMChat, config: dict[str, str]
    ) -> str | AsyncIterator[str]:
        provider = __map__[config["provider"]]
        client = AsyncClient(provider=provider)
        stream = provider.supports_stream
        # proxy_url = await srv.proxy.get_proxy_url()
        completion = client.chat.completions.create(
            model=config["model"],
            messages=chat,  # type: ignore
            stream=stream,
            # proxy=proxy_url,
        )

        if isinstance(completion, AsyncIterator):

            async def streaming():
                async for chunk in completion:
                    message = chunk.choices[0].delta.content
                    if message:
                        yield message

            return streaming()
        else:
            responce = await completion
            message = responce.choices[0].message.content
            if not message:
                raise LLMError("LLM returned empty result")
            return message

    @staticmethod
    def is_appropriate(
        provider: ProviderType,
    ) -> bool:
        return (
            provider.working
            and not provider.needs_auth
            and isinstance(provider, type)
            and issubclass(provider, AbstractProvider)
            and not ("webdriver" in provider.get_parameters())
        )


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
