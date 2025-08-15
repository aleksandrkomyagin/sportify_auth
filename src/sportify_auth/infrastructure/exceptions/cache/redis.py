from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException


class RedisConnectionException(BaseInfraException):
	status_code: int = 503


class RedisOperationException(BaseInfraException):
	status_code: int = 500
