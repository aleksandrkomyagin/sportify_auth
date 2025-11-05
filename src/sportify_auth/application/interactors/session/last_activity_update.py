from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.session import SessionLastActivityUpdateException
from sportify_auth.application.protocols.services import ISessionService
from sportify_auth.application.schemas.requests import SessionLastActivityUpdateRequestSchema
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class SessionLastActivityUpdateInteractor:
	def __init__(
		self,
		session_service: ISessionService,
	):
		self._session_service = session_service

	async def __call__(self, request_data: SessionLastActivityUpdateRequestSchema) -> None:
		logger.info("Новый запрос на обновление поля last_activity для DeviceId: %s", request_data.device_id)
		try:
			session = await self._session_service.update_session(request_data)
		except (BaseAppException, BaseInfraException) as e:
			raise SessionLastActivityUpdateException(
				status_code=e.status_code,
				message="Ошибка обновления поля last_activity",
				detail=str(e.message),
			) from e

		logger.info(
            "Успешный запрос на обновление поля last_activity. UserId: %s, DeviceId: %s",
            session.user_id,
            session.device_id
        )
