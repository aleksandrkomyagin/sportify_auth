from sportify_auth.application.dto.session import (
	DeviceInfoDTO,
	SessionDTO,
	SessionDeleteDTO,
)
from sportify_auth.application.dto.token import TokenData
from sportify_auth.application.dto.user import UserIdDTO
from sportify_auth.application.protocols.repositories.session.types import (
	DeviceData,
	SessionData,
	SessionEvent,
)


class SessionMapper:
	@staticmethod
	def to_dict_session(
		device_info: DeviceInfoDTO, user_id: UserIdDTO, token_data: TokenData
	) -> SessionData:
		return {
			"user_id": str(user_id.id),
			"device_id": str(device_info.id),
			"refresh_token": token_data.token,
			"expires_at": token_data.expires_at,
		}

	@staticmethod
	def to_dict_device(device_info: DeviceInfoDTO, user_id: UserIdDTO) -> DeviceData:
		return {
			"id": str(device_info.id),
			"user_id": str(user_id.id),
			"device_type": device_info.device_type,
			"device_name": device_info.device_name,
			"os_version": device_info.os_version,
			"push_token": device_info.push_token,
		}

	@staticmethod
	def to_dict_event(session: SessionDTO | SessionDeleteDTO, event_type: str) -> SessionEvent:
		return {
			"user_id": str(session.user_id),
			"device_id": str(session.device_id),
			"event": event_type,
		}
