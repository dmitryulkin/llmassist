from abc import ABC, abstractmethod

from pydantic import BaseModel


class ProxyProvider(BaseModel, ABC):
    rate: int = 0

    @abstractmethod
    def get_address(self) -> str:
        pass

    @abstractmethod
    def check(self) -> None:
        pass
