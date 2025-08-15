from sportify_auth.application.common.exceptions.base import BaseAppException, BaseDetailException


class TokenExpiredException(BaseAppException):
	status_code: int = 401


class InvalidTokenException(BaseAppException):
	status_code: int = 401


class TokenIsRevokedException(BaseAppException):
	status_code: int = 401


class InvalidTokenJTIException(BaseAppException):
	status_code: int = 401


class InvalidTokenTypeException(BaseAppException):
	status_code: int = 401


class InvalidTokenIssuerException(BaseAppException):
	status_code: int = 401


class JWKNotFoundException(BaseAppException):
	status_code: int = 401


class JWKGenerationException(BaseDetailException):
	pass


class JWKSNotFoundException(BaseAppException):
	status_code: int = 503


class MakeTokenException(BaseAppException):
	status_code: int = 503


class RSAKeyNotFoundException(BaseAppException):
	status_code: int = 503


class TokenRevocationException(BaseDetailException):
	pass


class TokenRefreshException(BaseDetailException):
	pass
