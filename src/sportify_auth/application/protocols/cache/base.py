from abc import abstractmethod
from typing import Any, Protocol


class ICacheService(Protocol):
	@abstractmethod
	async def set(
		self, db_name: str, key: str, value: Any, expire: int | None = None
	) -> None:
		pass

	@abstractmethod
	async def append(
			self,
			db_name: str,
			key: str,
			value: Any,
	) -> None:
		pass

	@abstractmethod
	async def get(self, db_name: str, key: str) -> Any | None:
		pass

	@abstractmethod
	async def delete(self, db_name: str, key: str) -> None:
		pass

	@abstractmethod
	async def exists(self, db_name: str, key: str) -> bool:
		pass

	@abstractmethod
	async def keys(self, db_name: str, pattern: str = "*") -> list[str]:
		pass

	@abstractmethod
	async def flush_db(self, db_name: str) -> None:
		pass
