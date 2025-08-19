from abc import abstractmethod
from typing import Protocol

from sportify_auth.application.dto.session import (
	DeviceIdDTO,
	DeviceInfoDTO,
	SessionDTO,
	SessionIdDTO,
)
from sportify_auth.application.protocols.repositories.session.types import (
	DeviceData,
	SessionData,
	SessionEvent,
)


class ISessionRepository(Protocol):
	@abstractmethod
	async def upsert_session(self, session_data: SessionData) -> SessionDTO:
		raise NotImplementedError

	@abstractmethod
	async def delete_session(
		self, session_ids: list[str], delete_devices: bool
	) -> tuple[list[SessionIdDTO], list[DeviceIdDTO]]:
		raise NotImplementedError

	@abstractmethod
	async def add_device(self, device_data: DeviceData) -> DeviceInfoDTO:
		raise NotImplementedError

	@abstractmethod
	async def get_device_by_id(self, device_id: str) -> DeviceInfoDTO:
		raise NotImplementedError

	@abstractmethod
	async def log_event(self, events: list[SessionEvent]) -> None:
		raise NotImplementedError
