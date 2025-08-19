import secrets

from sportify_auth.application.exceptions.confirmation_code import (
	ConfirmationCodeHasExpiredException,
	InvalidConfirmationCodeException,
)
from sportify_auth.application.protocols.cache import ICacheService
from sportify_auth.application.protocols.services import IConfirmationCodeService
from sportify_auth.setup.config import settings


class ConfirmationCodeService(IConfirmationCodeService):
	def __init__(
		self,
		cache: ICacheService,
	) -> None:
		self._cache = cache

	async def get_code(self, key_prefix: str, phone: str) -> str:
		code = "".join(secrets.choice("0123456789") for _ in range(6))
		await self._cache.set(settings.redis.code_db, f"{key_prefix}:{phone}", code, 300)
		return code

	async def validate_code(self, key_prefix: str, phone: str, expected_code: str) -> None:
		code = await self._cache.get(settings.redis.code_db, f"{key_prefix}:{phone}")
		if code is None:
			raise ConfirmationCodeHasExpiredException(
				message="Срок действия кода подтверждения истек, запросите новый",
			)
		if str(code) != expected_code:
			raise InvalidConfirmationCodeException(
				message="Неверный код подтверждения, запросите новый"
			)
