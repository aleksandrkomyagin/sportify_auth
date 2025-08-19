from abc import abstractmethod
from typing import Protocol


class IConfirmationCodeService(Protocol):
	@abstractmethod
	async def get_code(self, key_prefix: str, phone: str) -> str:
		pass

	@abstractmethod
	async def validate_code(self, key_prefix: str, phone: str, expected_code: str) -> None:
		pass
