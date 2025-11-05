from abc import abstractmethod
from typing import Protocol

from sportify_auth.application.dto.event import NewOutboxEventDTO
from sportify_auth.application.dto.session import DeviceInfoDTO, SessionDTO, SessionIdDTO
from sportify_auth.application.dto.token import TokenData
from sportify_auth.application.dto.user import UserIdDTO
from sportify_auth.application.schemas.requests import SessionLastActivityUpdateRequestSchema


class ISessionService(Protocol):
	@abstractmethod
	async def new_session(
		self,
		device_info: DeviceInfoDTO,
		user_id: UserIdDTO,
		token: TokenData,
		event_type: str,
	) -> NewOutboxEventDTO:
		raise NotImplementedError

	@abstractmethod
	async def revoke_session(
		self,
		session_ids: list[SessionIdDTO],
		user_id: UserIdDTO,
		delete_devices: bool = False,
	) -> NewOutboxEventDTO:
		raise NotImplementedError

	@abstractmethod
	async def update_session(self, device_id: SessionLastActivityUpdateRequestSchema) -> SessionDTO:
		raise NotImplementedError
