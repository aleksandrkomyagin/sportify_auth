import logging

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.user import UserSignInException
from sportify_auth.application.protocols.services import IUserService
from sportify_auth.application.schemas.requests import UserSignInRequestSchema
from sportify_auth.application.schemas.responses import UserSignInResponseSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = logging.getLogger(__name__)


class UserSignInInteractor:
	def __init__(self, user_service: IUserService):
		self._user_service = user_service

	async def __call__(
		self, request_data: UserSignInRequestSchema
	) -> UserSignInResponseSchema:
		logger.info("Новый запрос на аутентификацию")
		try:
			user_id = await self._user_service.signin(request_data)
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserSignInException(
				status_code=e.status_code,
				message="Ошибка аутентификации пользователя",
				detail=str(e.message),
			) from e

		logger.info("Успешный запрос на аутентификацию. UserId: %s", user_id)
		return UserSignInResponseSchema(message="Отправлен код подтверждения")
