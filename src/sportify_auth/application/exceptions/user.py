from sportify_auth.application.common.exceptions.base import BaseAppException, BaseDetailException


class UserNotFoundException(BaseAppException):
	status_code: int = 404


class UserSignupSessionHasExpiredException(BaseAppException):
	status_code: int = 410


class UserSignUpException(BaseDetailException):
	pass


class UserSignUpConfirmException(BaseDetailException):
	pass


class UserSignInException(BaseDetailException):
	pass


class UserSignInConfirmException(BaseDetailException):
	pass


class UserActivationException(BaseDetailException):
	pass


class UserActivationConfirmException(BaseDetailException):
	pass


class UserDeactivationException(BaseDetailException):
	pass


class UserDeleteException(BaseDetailException):
	pass
