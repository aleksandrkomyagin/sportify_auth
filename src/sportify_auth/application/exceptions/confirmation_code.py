from sportify_auth.application.common.exceptions.base import BaseAppException


class ConfirmationCodeHasExpiredException(BaseAppException):
	status_code: int = 410


class InvalidConfirmationCodeException(BaseAppException):
	status_code: int = 400
