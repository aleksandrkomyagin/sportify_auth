from logging import getLogger

from sportify_auth.adapters.mappers.session_mapper import SessionMapper
from sportify_auth.application.dto.event import NewOutboxEventDTO
from sportify_auth.application.dto.session import (
	DeviceInfoDTO, SessionDeleteDTO,
	SessionDTO, SessionIdDTO,
)
from sportify_auth.application.dto.token import TokenData
from sportify_auth.application.dto.user import UserIdDTO
from sportify_auth.application.protocols.repositories import ISessionRepository
from sportify_auth.application.protocols.services import ISessionService
from sportify_auth.application.schemas.requests import SessionLastActivityUpdateRequestSchema

logger = getLogger(__name__)


class SessionService(ISessionService):
	def __init__(self, session_repository: ISessionRepository) -> None:
		self._session_repository = session_repository

	async def new_session(
		self,
		device_info: DeviceInfoDTO,
		user_id: UserIdDTO,
		token: TokenData,
		event_type: str,
	) -> NewOutboxEventDTO:
		new_device = False
		device = await self._session_repository.get_device_by_id(device_info.id)
		if not device:
			device = await self._session_repository.add_device(
				SessionMapper.to_dict_device(device_info)
			)
			new_device = True
		await self._session_repository.attach_device_to_user(device.id, user_id.id)
		session = await self._session_repository.upsert_session(
			SessionMapper.to_dict_session(device, user_id, token)
		)
		await self._session_repository.log_event([SessionMapper.to_dict_event(session, event_type)])

		return NewOutboxEventDTO(
			topic="new_session",
			payload={
				"session_id": session.session_id,
				"user_id": session.user_id,
				"device_id": session.device_id,
				"refresh_token": session.refresh_token,
				"expires_at": session.expires_at.isoformat(),
				"last_activity": session.last_activity.isoformat(),
				"created_at": session.created_at.isoformat(),
				"new_device": {
					"device_id": device.id,
					"device_type": device.device_type,
					"device_name": device.device_name,
					"os_version": device.os_version,
					"push_token": device.push_token,
					"created_at": device.created_at.isoformat(),
				}
				if new_device
				else {},
			},
		)

	async def revoke_session(
		self,
		session_ids: list[SessionIdDTO],
		user_id: UserIdDTO,
		delete_devices: bool = False,
	) -> NewOutboxEventDTO:
		(
			delete_session_ids,
			delete_devices_ids,
		) = await self._session_repository.delete_session(
			[str(session_id.session_id) for session_id in session_ids], delete_devices
		)

		await self._session_repository.log_event(
			[
				SessionMapper.to_dict_event(
					SessionDeleteDTO(user_id=str(user_id.id), device_id=str(device_id.device_id)),
					"sign_out",
				)
				for device_id in delete_devices_ids
			]
		)
		return NewOutboxEventDTO(
			topic="delete_session",
			payload={
				"delete_session_ids": [session_id.session_id for session_id in delete_session_ids],
				"delete_device_ids": [device_id.device_id for device_id in delete_devices_ids]
				if delete_devices
				else [],
			},
		)

	async def update_session(self, device_id: SessionLastActivityUpdateRequestSchema) -> SessionDTO:
		return await self._session_repository.update_last_activity(device_id.device_id)
