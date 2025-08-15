from abc import abstractmethod
from typing import Any, Protocol

from sportify_auth.application.dto.rsa_key import RSAKeyDTO


class IKeyGenerator(Protocol):

    @abstractmethod
    async def generate_rsa(self) -> RSAKeyDTO:
        pass

    @abstractmethod
    async def generate_public_key_from_jwk(self, jwk: dict[str, Any]) -> str:
        pass
