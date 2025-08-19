from abc import abstractmethod
from typing import Protocol


class ITaskManager(Protocol):
	@abstractmethod
	async def start(self) -> None:
		pass

	@abstractmethod
	async def stop(self) -> None:
		pass

	@abstractmethod
	async def delay_by_time(self, task_name: str, *args) -> None:
		pass
