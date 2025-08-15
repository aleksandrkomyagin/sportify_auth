from abc import abstractmethod
from typing import Protocol

from sportify_auth.application.dto.event import OutboxEventDTO
from sportify_auth.application.protocols.repositories.outbox_event.types import EventData


class IOutboxRepository(Protocol):

    @abstractmethod
    async def create_event(self, event: EventData) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_events(self, limit: int = 100) -> list[OutboxEventDTO]:
        raise NotImplementedError

    @abstractmethod
    async def update_events(self, event_ids: list[int], status: str) -> None:
        raise NotImplementedError
