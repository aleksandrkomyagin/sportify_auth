from abc import abstractmethod
from typing import Protocol

from sportify_auth.application.dto.event import NewOutboxEventDTO, OutboxEventDTO


class IOutboxService(Protocol):
	@abstractmethod
	async def save_event(self, event: NewOutboxEventDTO) -> None:
		pass

	@abstractmethod
	async def get_not_processed_events(self) -> list[OutboxEventDTO]:
		pass

	@abstractmethod
	async def change_event_statuses(self, event_ids: list[int], status: str) -> None:
		pass
