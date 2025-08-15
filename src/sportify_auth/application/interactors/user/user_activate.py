from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.user import UserActivationException
from sportify_auth.application.protocols.services import IUserService
from sportify_auth.application.schemas.requests import UserActivateRequestSchema
from sportify_auth.application.schemas.responses import UserActivateResponseSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class UserActivateInteractor:
	def __init__(
		self,
		user_service: IUserService,
	):
		self._user_service = user_service

	async def __call__(
		self, request_data: UserActivateRequestSchema
	) -> UserActivateResponseSchema:
		logger.info("Новый запрос на активацию пользователя")
		try:
			user_id = await self._user_service.user_activate(request_data)
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserActivationException(
				status_code=e.status_code,
				message="Ошибка активации пользователя",
				detail=str(e.message),
			) from e

		logger.info("Успешный запрос на активацию пользователя. UserId: %s", user_id)
		return UserActivateResponseSchema(message="Отправлен код подтверждения")
