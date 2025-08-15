from dataclasses import dataclass, field


@dataclass(eq=False)
class BaseDomainException(Exception):
	"""Base Domain Error."""

	status_code: int = field(init=False)
	message: str

	def __str__(self):
		return f"{self.__class__.__name__}: {self.message}"
