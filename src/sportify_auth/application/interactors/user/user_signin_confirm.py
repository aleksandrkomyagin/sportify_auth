from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.dto.session import DeviceInfoDTO
from sportify_auth.application.dto.user import UserSignInConfirmRequest
from sportify_auth.application.exceptions.user import UserSignInConfirmException
from sportify_auth.application.protocols.repositories import ITransactionManager
from sportify_auth.application.protocols.services import (
	IOutboxService,
	ISessionService,
	ITokenService,
	IUserService,
)
from sportify_auth.application.schemas.requests import UserSignInConfirmRequestSchema
from sportify_auth.application.schemas.responses import UserSignInConfirmResponseSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class UserSignInConfirmInteractor:
	def __init__(
		self,
		user_service: IUserService,
		outbox_service: IOutboxService,
		token_service: ITokenService,
		session_service: ISessionService,
		tm: ITransactionManager,
	):
		self._user_service = user_service
		self._outbox_service = outbox_service
		self._token_service = token_service
		self._session_service = session_service
		self._tm = tm

	async def __call__(
		self, request_data: UserSignInConfirmRequestSchema
	) -> UserSignInConfirmResponseSchema:
		logger.info("Новый запрос на подтверждение аутентификации")
		try:
			async with self._tm as tm:
				user_id = await self._user_service.signin_confirm(
					UserSignInConfirmRequest(
						phone=request_data.signin_confirm_data.phone,
						code=request_data.signin_confirm_data.code,
					)
				)
				token = await self._token_service.create_token(user_id)
				event = await self._session_service.new_session(
					DeviceInfoDTO(
						device_name=request_data.device_info.device_name,
						device_type=request_data.device_info.device_type,
						device_id=request_data.device_info.device_id,
						os_version=request_data.device_info.os_version,
						push_token=request_data.device_info.push_token,
					),
					user_id,
					token.refresh_token,
					"signin",
				)
				await self._outbox_service.save_event(event)
				await tm.commit()
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserSignInConfirmException(
				status_code=e.status_code,
				message="Ошибка подтверждения аутентификации пользователя",
				detail=str(e.message),
			) from e

		logger.info("Успешный запрос на подтверждение аутентификации. UserId: %s", user_id)
		return UserSignInConfirmResponseSchema(
			access_token=token.access_token.token, refresh_token=token.refresh_token.token
		)
