import uuid

from dataclasses import dataclass

from sportify_auth.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserUUID(ValueObject[str]):
	def __post_init__(self):
		uuid.UUID(self.value)
