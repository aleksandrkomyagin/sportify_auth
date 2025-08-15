from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException


class StartEngineException(BaseInfraException):
	status_code: int = 503


class DatabaseOperationException(BaseInfraException):
	status_code: int = 500
