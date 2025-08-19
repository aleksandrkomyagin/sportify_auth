import re

from dataclasses import dataclass

from sportify_auth.domain.common.value_objects.base import ValueObject
from sportify_auth.domain.exceptions.user import (
	EmptyExceptionBase,
	InvalidFormatException,
)

PHONE_REGEX = re.compile(r"^7\d{10}$")


@dataclass(frozen=True)
class Phone(ValueObject[str]):
	def _validate(self) -> None:
		if not self.value:
			raise EmptyExceptionBase(message="Поле не может быть пустым")
		if not PHONE_REGEX.match(self.value):
			raise InvalidFormatException(message="Неверный формат номера")
