from dataclasses import dataclass

from ..validator import ValidatedDataClass


@dataclass
class BaseTokenRequestSchema(ValidatedDataClass):
	refresh_token: str


@dataclass
class DeviceInfo:
	device_id: str
	device_type: str
	device_name: str
	os_version: str
	push_token: str


@dataclass
class RefreshTokenRequestSchema(BaseTokenRequestSchema):
	user_id: str
	device_info: DeviceInfo


class RevokeTokenRequestSchema(BaseTokenRequestSchema):
	pass
