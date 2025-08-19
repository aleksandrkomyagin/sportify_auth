import jwt

from sportify_auth.application.protocols.security.auth import IAuthenticateService
from sportify_auth.infrastructure.exceptions.security.service_token import (
	BearerSchemaRequiredException,
	InvalidTokenException,
	TokenExpiredException,
	TokenRequiredException,
)
from sportify_auth.setup.config import settings


def get_authorization_scheme_param(
	authorization_header_value: str | None,
) -> tuple[str, str]:
	scheme, param = authorization_header_value.split(" ")
	return scheme, param


class AuthenticateService(IAuthenticateService):
	def __call__(self, authorization_header: str | None) -> None:
		if authorization_header is None:
			raise TokenRequiredException(message="Не передан токен доступа")
		scheme, token = get_authorization_scheme_param(authorization_header)
		if scheme.lower() != "bearer":
			raise BearerSchemaRequiredException(message="Некорректная схема токена")
		if not token:
			raise TokenRequiredException(message="Не передан токен доступа")
		try:
			jwt.decode(
				token,
				settings.security.secret_key,
				algorithms=settings.security.algorithm,
			)
		except jwt.ExpiredSignatureError as e:
			raise TokenExpiredException(message="Срок действия токена доступа истек") from e
		except jwt.InvalidTokenError as e:
			raise InvalidTokenException(message="Некорректный токен доступа") from e
		except jwt.PyJWTError as e:
			raise InvalidTokenException(message="Некорректный токен доступа") from e
