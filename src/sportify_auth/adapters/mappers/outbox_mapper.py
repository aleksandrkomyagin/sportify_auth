from sportify_auth.application.dto.event import NewOutboxEventDTO
from sportify_auth.application.protocols.repositories.outbox_event.types import EventData


class EventMapper:
	@staticmethod
	def to_dict(event: NewOutboxEventDTO) -> EventData:
		return {
			"topic": event.topic,
			"payload": event.payload,
		}
