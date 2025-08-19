from logging import getLogger

from sportify_auth.adapters.mappers.outbox_mapper import EventMapper
from sportify_auth.application.dto.event import NewOutboxEventDTO, OutboxEventDTO
from sportify_auth.application.protocols.repositories import IOutboxRepository
from sportify_auth.application.protocols.services import IOutboxService

logger = getLogger(__name__)


class OutboxService(IOutboxService):
	def __init__(
		self,
		outbox_repository: IOutboxRepository,
	) -> None:
		self._outbox_repository = outbox_repository

	async def save_event(self, event: NewOutboxEventDTO) -> None:
		await self._outbox_repository.create_event(EventMapper.to_dict(event))
		logger.info("Новое событие: %s", EventMapper.to_dict(event))

	async def get_not_processed_events(self) -> list[OutboxEventDTO]:
		return await self._outbox_repository.get_events()

	async def change_event_statuses(self, event_ids: list[int], status: str) -> None:
		await self._outbox_repository.update_events(event_ids, status)
