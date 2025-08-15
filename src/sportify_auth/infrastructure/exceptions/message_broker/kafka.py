from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException


class StartProducerException(BaseInfraException):
	status_code: int = 500


class StartConsumerException(BaseInfraException):
	status_code: int = 500


class StopProducerException(BaseInfraException):
	status_code: int = 500


class StopConsumerException(BaseInfraException):
	status_code: int = 500


class SendMessageException(BaseInfraException):
	status_code: int = 500
