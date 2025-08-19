from abc import abstractmethod
from typing import Protocol

from sportify_auth.application.dto.event import NewOutboxEventDTO
from sportify_auth.application.dto.session import DeviceInfoDTO, SessionIdDTO
from sportify_auth.application.dto.token import TokenData
from sportify_auth.application.dto.user import UserIdDTO


class ISessionService(Protocol):
	@abstractmethod
	async def new_session(
		self,
		device_info: DeviceInfoDTO,
		user_id: UserIdDTO,
		token: TokenData,
		event_type: str,
	) -> NewOutboxEventDTO:
		pass

	@abstractmethod
	async def revoke_session(
		self,
		session_ids: list[SessionIdDTO],
		user_id: UserIdDTO,
		delete_devices: bool = False,
	) -> NewOutboxEventDTO:
		pass
