from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.user import UserActivationException
from sportify_auth.application.protocols.repositories import ITransactionManager
from sportify_auth.application.protocols.services import IOutboxService, IUserService
from sportify_auth.application.schemas.requests import UserActivateConfirmRequestSchema
from sportify_auth.application.schemas.responses import UserActivateConfirmResponseSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class UserActivateConfirmInteractor:
	def __init__(
			self,
			user_service: IUserService,
			outbox_service: IOutboxService,
			tm: ITransactionManager
	):
		self._user_service = user_service
		self._outbox_service = outbox_service
		self._tm = tm

	async def __call__(
		self, request_data: UserActivateConfirmRequestSchema
	) -> UserActivateConfirmResponseSchema:
		logger.info("Новый запрос на подтверждение активации пользователя")
		try:
			async with self._tm as tm:
				event, user_id = await self._user_service.user_activate_confirm(request_data)
				await self._outbox_service.save_event(event)
				await tm.commit()
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserActivationException(
				status_code=e.status_code,
				message="Ошибка подтверждения активации пользователя",
				detail=str(e.message),
			) from e

		logger.info("Успешный запрос на подтверждение активации пользователя. UserId: %s", user_id)
		return UserActivateConfirmResponseSchema(message="Пользователь активирован")
