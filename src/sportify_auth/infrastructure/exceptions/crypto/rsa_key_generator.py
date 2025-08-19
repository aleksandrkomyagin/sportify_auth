from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException


class RSAGenerationException(BaseInfraException):
	status_code: int = 503


class PublicKeyGenerationException(BaseInfraException):
	status_code: int = 503
