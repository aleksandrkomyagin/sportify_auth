from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.user import UserDeleteException
from sportify_auth.application.protocols.repositories import ITransactionManager
from sportify_auth.application.protocols.services import IOutboxService, IUserService
from sportify_auth.application.schemas.requests import UserDeleteRequestSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class UserDeleteInteractor:
	def __init__(
			self,
			user_service: IUserService,
			outbox_service: IOutboxService,
			tm: ITransactionManager
	):
		self._user_service = user_service
		self._outbox_service = outbox_service
		self._tm = tm

	async def __call__(self, request_data: UserDeleteRequestSchema) -> None:
		logger.info("Новый запрос на удаление пользователя")
		try:
			async with self._tm as tm:
				event, user_id = await self._user_service.delete_user(request_data)
				await self._outbox_service.save_event(event)
				await tm.commit()
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserDeleteException(
				status_code=e.status_code,
				message="Ошибка удаления пользователя",
				detail=str(e.message)
			) from e
		logger.info("Успешный запрос на удаление пользователя. UserId: %s", user_id)
