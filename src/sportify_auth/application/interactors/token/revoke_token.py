from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.token import TokenRevocationException
from sportify_auth.application.protocols.services import IOutboxService, ITokenService
from sportify_auth.application.schemas.requests import RevokeTokenRequestSchema
from sportify_auth.application.schemas.responses import RevokeTokenResponseSchema
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException


class RevokeTokenInteractor:
	def __init__(self, token_service: ITokenService, outbox_service: IOutboxService):
		self._token_service = token_service
		self._outbox_service = outbox_service

	async def __call__(self, request_data: RevokeTokenRequestSchema) -> RevokeTokenResponseSchema:
		try:
			event = await self._token_service.revoke_token(request_data)
			await self._outbox_service.save_event(event)
		except (BaseAppException, BaseInfraException) as e:
			raise TokenRevocationException(
				status_code=e.status_code,
				message="Ошибка отзыва токена",
				detail=str(e.message),
			) from e

		return RevokeTokenResponseSchema(message="Токен отозван")
