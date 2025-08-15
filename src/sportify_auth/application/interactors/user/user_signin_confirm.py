from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.user import UserSignInConfirmException
from sportify_auth.application.protocols.services import ITokenService, IUserService
from sportify_auth.application.schemas.requests import UserSignInConfirmRequestSchema
from sportify_auth.application.schemas.responses import UserSignInConfirmResponseSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class UserSignInConfirmInteractor:
	def __init__(self, user_service: IUserService, token_service: ITokenService):
		self._user_service = user_service
		self._token_service = token_service

	async def __call__(
		self, request_data: UserSignInConfirmRequestSchema
	) -> UserSignInConfirmResponseSchema:
		logger.info("Новый запрос на подтверждение аутентификации")
		try:
			user_id = await self._user_service.signin_confirm(request_data)
			token = await self._token_service.create_token(user_id)
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserSignInConfirmException(
				status_code=e.status_code,
				message="Ошибка подтверждения аутентификации пользователя",
				detail=str(e.message),
			) from e

		logger.info("Успешный запрос на подтверждение аутентификации. UserId: %s", user_id)
		return UserSignInConfirmResponseSchema(
			access_token=token.access_token, refresh_token=token.refresh_token
		)
