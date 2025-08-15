from abc import abstractmethod
from types import TracebackType
from typing import Protocol, Self


class ITransactionManager(Protocol):
	@abstractmethod
	async def __aenter__(self) -> Self:
		pass

	@abstractmethod
	async def __aexit__(
		self,
		exc_type: type[BaseException],
		exc_val: BaseException,
		exc_tb: TracebackType,
	):
		pass

	@abstractmethod
	async def commit(self):
		pass

	@abstractmethod
	async def rollback(self):
		pass
