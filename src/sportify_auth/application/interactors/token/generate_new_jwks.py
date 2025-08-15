from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.token import JWKGenerationException
from sportify_auth.application.protocols.services import ITokenService
from sportify_auth.application.protocols.task_manager.base import ITaskManager
from sportify_auth.application.schemas.responses import GenerateNewJWKSResponseSchema
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class GenerateNewJWKSInteractor:
	def __init__(self, token_service: ITokenService, task_manager: ITaskManager):
		self._token_service = token_service
		self._task_manager = task_manager

	async def __call__(self) -> GenerateNewJWKSResponseSchema:
		try:
			kid = await self._token_service.generate_new_rsa_key()
			await self._task_manager.delay_by_time("delete_expired_jwk", kid)
		except (BaseAppException, BaseInfraException) as e:
			logger.error("Ошибка генерации JWKS: %s", e, exc_info=True)
			raise JWKGenerationException(
				status_code=e.status_code, message="Ошибка генерации JWKS", detail=str(e.message)
			) from e

		return GenerateNewJWKSResponseSchema(message="Новый JWKS сгенерирован")
