from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DeviceInfoDTO:
	id: str
	device_name: str
	device_type: str
	os_version: str
	push_token: str
	created_at: datetime = field(init=False)

	def __init__(
		self,
		device_id: str,
		device_name: str,
		device_type: str,
		os_version: str,
		push_token: str,
		created_at: datetime | None = None,
	):
		self.id = device_id
		self.device_name = device_name
		self.device_type = device_type
		self.os_version = os_version
		self.push_token = push_token
		if created_at is not None:
			self.created_at = created_at


@dataclass
class DeviceIdDTO:
	device_id: str


@dataclass
class SessionDTO:
	session_id: str
	user_id: str
	device_id: str
	refresh_token: str
	expires_at: datetime
	last_activity: datetime
	created_at: datetime


@dataclass
class SessionDeleteDTO:
	user_id: str
	device_id: str


@dataclass
class SessionIdDTO:
	session_id: str
