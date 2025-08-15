from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.user import UserSignUpException
from sportify_auth.application.protocols.repositories import ITransactionManager
from sportify_auth.application.protocols.services import IUserService
from sportify_auth.application.schemas.requests import UserSignUpRequestSchema
from sportify_auth.application.schemas.responses import UserSignUpResponseSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class UserSignUpInteractor:
	def __init__(
		self,
		user_service: IUserService,
		tm: ITransactionManager
	):
		self._user_service = user_service
		self._tm = tm

	async def __call__(
		self, request_data: UserSignUpRequestSchema
	) -> UserSignUpResponseSchema:
		logger.info("Новый запрос на регистрацию")
		try:
			async with self._tm as tm:
				user_id = await self._user_service.signup(request_data)
				await tm.commit()
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserSignUpException(
				status_code=e.status_code,
				message="Ошибка регистрации пользователя",
				detail=str(e.message),
			) from e
		logger.info("Успешная запрос на регистрацию. UserId: %s", user_id)
		return UserSignUpResponseSchema(message="Отправлен код подтверждения")
