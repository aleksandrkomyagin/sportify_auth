from abc import abstractmethod
from typing import Any, Protocol


class IJWKStorage(Protocol):
    @abstractmethod
    async def add(self, jwks: list[dict[str, Any]]) -> None:
        pass

    @abstractmethod
    async def replace(self, jwks: list[dict[str, Any]]) -> None:
        pass
