from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from pydantic import BaseModel


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
