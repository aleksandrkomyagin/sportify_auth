from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.token import TokenRefreshException
from sportify_auth.application.protocols.services import ITokenService
from sportify_auth.application.schemas.requests import RefreshTokenRequestSchema
from sportify_auth.application.schemas.responses import RefreshTokenResponseSchema
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException


class RefreshTokenInteractor:
	def __init__(self, token_service: ITokenService):
		self._token_service = token_service

	async def __call__(
		self, request_data: RefreshTokenRequestSchema
	) -> RefreshTokenResponseSchema:
		try:
			token = await self._token_service.refresh_token(request_data)
		except (BaseAppException, BaseInfraException) as e:
			raise TokenRefreshException(
				status_code=e.status_code, message="Ошибка обновления токена", detail=str(e.message)
			) from e

		return RefreshTokenResponseSchema(
			access_token=token.access_token, refresh_token=token.refresh_token
		)
