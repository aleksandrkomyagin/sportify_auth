from dataclasses import dataclass

from ..validator import ValidatedDataClass


@dataclass
class SessionLastActivityUpdateRequestSchema(ValidatedDataClass):
	device_id: str
