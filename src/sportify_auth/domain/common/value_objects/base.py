from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T", bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC):
	def __post_init__(self) -> None:
		self._validate()

	def _validate(self) -> None:
		pass


@dataclass(frozen=True)
class ValueObject(BaseValueObject, ABC, Generic[T]):
	value: T

	def to_raw(self) -> T:
		return self.value
