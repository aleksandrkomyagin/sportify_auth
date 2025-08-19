from datetime import datetime
from typing import TypedDict


class SessionData(TypedDict):
	user_id: str
	device_id: str
	refresh_token: str
	expires_at: datetime


class DeviceData(TypedDict):
	id: str
	user_id: str
	device_type: str
	device_name: str
	os_version: str
	push_token: str


class SessionEvent(TypedDict):
	user_id: str
	device_id: str
	event: str
