from sportify_auth.domain.common.exceptions.base import BaseDomainException


class EmptyExceptionBase(BaseDomainException):
	status_code: int = 400


class PhoneAlreadyExistsException(BaseDomainException):
	status_code: int = 400


class InactiveUserException(BaseDomainException):
	status_code: int = 403


class InvalidFormatException(BaseDomainException):
	status_code: int = 400
