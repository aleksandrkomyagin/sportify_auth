from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.dto.session import SessionIdDTO
from sportify_auth.application.dto.user import UserIdDTO
from sportify_auth.application.exceptions.user import UserSignOutException
from sportify_auth.application.protocols.repositories import ITransactionManager
from sportify_auth.application.protocols.services import IOutboxService, ISessionService
from sportify_auth.application.schemas.requests import UserSignOutRequestSchema
from sportify_auth.application.schemas.responses import UserSignOutResponseSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class UserSignOutInteractor:
	def __init__(
		self,
		session_service: ISessionService,
		outbox_service: IOutboxService,
		tm: ITransactionManager,
	):
		self._session_service = session_service
		self._outbox_service = outbox_service
		self._tm = tm

	async def __call__(self, request_data: UserSignOutRequestSchema) -> UserSignOutResponseSchema:
		logger.info("Новый запрос на выход из устройства")
		try:
			async with self._tm as tm:
				event = await self._session_service.revoke_session(
					[SessionIdDTO(session_id) for session_id in request_data.session_ids],
					UserIdDTO(request_data.user_id),
					delete_devices=request_data.delete_devices,
				)
				await self._outbox_service.save_event(event)
				await tm.commit()
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserSignOutException(
				status_code=e.status_code,
				message="Ошибка выхода из устройства",
				detail=str(e.message),
			) from e
		logger.info("Успешный запрос на выход из устройства. UserId: %s", request_data.user_id)
		return UserSignOutResponseSchema(message="Выход успешно выполнен")
