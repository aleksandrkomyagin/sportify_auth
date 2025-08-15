from logging import getLogger

from sportify_auth.application.common.exceptions.base import BaseAppException
from sportify_auth.application.exceptions.user import UserSignUpConfirmException
from sportify_auth.application.protocols.repositories import ITransactionManager
from sportify_auth.application.protocols.services import IOutboxService, ITokenService, IUserService
from sportify_auth.application.schemas.requests import UserSignUpConfirmRequestSchema
from sportify_auth.application.schemas.responses import UserSignUpConfirmResponseSchema
from sportify_auth.domain.common.exceptions.base import BaseDomainException
from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException

logger = getLogger(__name__)


class UserSignUpConfirmInteractor:
	def __init__(
		self,
		user_service: IUserService,
		outbox_service: IOutboxService,
		token_service: ITokenService,
		tm: ITransactionManager
	):
		self._user_service = user_service
		self._outbox_service = outbox_service
		self._token_service = token_service
		self._tm = tm

	async def __call__(
		self, request_data: UserSignUpConfirmRequestSchema
	) -> UserSignUpConfirmResponseSchema:
		logger.info("Новый запрос на подтверждение регистрации")
		try:
			async with self._tm as tm:
				event, user_id = await self._user_service.signup_confirm(request_data)
				await self._outbox_service.save_event(event)
				token = await self._token_service.create_token(user_id)
				await tm.commit()
		except (BaseAppException, BaseDomainException, BaseInfraException) as e:
			raise UserSignUpConfirmException(
				status_code=e.status_code,
				message="Ошибка подтверждения регистрации пользователя",
				detail=str(e.message),
			) from e

		logger.info("Успешный запрос на подтверждение регистрации. UserId: %s", user_id)
		return UserSignUpConfirmResponseSchema(
			access_token=token.access_token, refresh_token=token.refresh_token
		)
