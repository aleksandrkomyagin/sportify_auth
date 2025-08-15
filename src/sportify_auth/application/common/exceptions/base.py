from dataclasses import dataclass, field
from typing import Any


@dataclass(eq=False)
class BaseAppException(Exception):
	"""Base Application Error."""

	message: str
	status_code: int = field(init=False)

	def __str__(self):
		return f"{self.__class__.__name__}: {self.message}"


@dataclass(eq=False)
class BaseDetailException(BaseAppException):
	"""Base Detail Exception."""
	detail: str
	status_code: int
	response_data: dict[str, Any] = field(init=False)

	def __post_init__(self):
		self.response_data = {
			"status": False,
			"message": self.message,
			"detail": {"text": self.detail},
		}
