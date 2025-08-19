from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.dto.session import DeviceInfoDTO
from sportify_auth.application.dto.token import RefreshTokenRequest
from sportify_auth.application.dto.user import UserIdDTO
from sportify_auth.application.exceptions.token import TokenRefreshException
from sportify_auth.application.protocols.repositories import ITransactionManager
from sportify_auth.application.protocols.services import (
	IOutboxService,
	ISessionService,
	ITokenService,
)
from sportify_auth.application.schemas.requests import RefreshTokenRequestSchema
from sportify_auth.application.schemas.responses import RefreshTokenResponseSchema
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException


class RefreshTokenInteractor:
	def __init__(
		self,
		outbox_service: IOutboxService,
		token_service: ITokenService,
		session_service: ISessionService,
		tm: ITransactionManager,
	):
		self._outbox_service = outbox_service
		self._token_service = token_service
		self._session_service = session_service
		self._tm = tm

	async def __call__(self, request_data: RefreshTokenRequestSchema) -> RefreshTokenResponseSchema:
		try:
			async with self._tm as tm:
				token = await self._token_service.refresh_token(
					RefreshTokenRequest(request_data.refresh_token)
				)
				event = await self._session_service.new_session(
					DeviceInfoDTO(
						device_name=request_data.device_info.device_name,
						device_type=request_data.device_info.device_type,
						device_id=request_data.device_info.device_id,
						os_version=request_data.device_info.os_version,
						push_token=request_data.device_info.push_token,
					),
					UserIdDTO(request_data.user_id),
					token.refresh_token,
					"token_refresh",
				)
				await self._outbox_service.save_event(event)
				await tm.commit()
		except (BaseAppException, BaseInfraException) as e:
			raise TokenRefreshException(
				status_code=e.status_code,
				message="Ошибка обновления токена",
				detail=str(e.message),
			) from e

		return RefreshTokenResponseSchema(
			access_token=token.access_token.token, refresh_token=token.refresh_token.token
		)
