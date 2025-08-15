from dataclasses import dataclass

from sportify_auth.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class IsActive(ValueObject[bool]):
	pass
