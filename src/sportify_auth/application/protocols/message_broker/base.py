from abc import abstractmethod
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class IMessageProducer(Protocol):
	@abstractmethod
	async def send(self, topic: str, message: dict, key: str | None = None) -> None:
		pass

	@abstractmethod
	async def send_and_wait(self, topic: str, message: dict, key: str | None = None) -> None:
		pass

	@abstractmethod
	async def start(self) -> None:
		pass

	@abstractmethod
	async def stop(self) -> None:
		pass


class IMessageConsumer(Protocol):
	@abstractmethod
	async def start(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
		pass

	@abstractmethod
	async def stop(self) -> None:
		pass
