from abc import ABC, abstractmethod

from pydantic import BaseModel


class ProxyProvider(BaseModel, ABC):
    rate: int = 0

    @abstractmethod
    async def check(self) -> bool:
        pass

    @abstractmethod
    async def get_address(self) -> str:
        pass
