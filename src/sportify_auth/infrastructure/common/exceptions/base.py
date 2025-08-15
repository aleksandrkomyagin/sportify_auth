from dataclasses import dataclass, field


@dataclass(eq=False)
class BaseInfraException(Exception):
	"""Base Infrastructure Error."""

	status_code: int = field(init=False)
	message: str

	def __str__(self):
		return f"{self.__class__.__name__}: {self.message}"


@dataclass(eq=False)
class BaseServiceAuthException(Exception):
	status_code: int = field(init=False)
	message: str

	def __str__(self):
		return f"{self.__class__.__name__}: {self.message}"
