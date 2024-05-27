from abc import ABC, abstractmethod

from g4f.Provider import ProviderType, __map__, __providers__
from g4f.providers.base_provider import ProviderModelMixin
from loguru import logger
from pydantic import BaseModel

from src.utils.settings import Settings


class LLMService(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass

    @abstractmethod
    def get_providers(self) -> list[str]:
        """
        Return a list of all working providers.
        """
        pass

    @abstractmethod
    def get_provider_models(self, provider_name: str) -> list[str]:
        """
        Return a list of all working models for provider.
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

    @staticmethod
    def is_appropriate(
        provider: ProviderType,
    ) -> bool:
        return provider.working and not provider.needs_auth


class LLM(BaseModel):
    settings: Settings
    services: dict[str, LLMService] = {}

    def init(self):
        logger.info("LLM init...")
        self.services[GPT4FreeLLMService.get_name()] = GPT4FreeLLMService()
        logger.info("LLM init done")
