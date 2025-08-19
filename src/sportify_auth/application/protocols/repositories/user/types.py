from datetime import datetime
from typing import NotRequired, TypedDict


class UserData(TypedDict):
	id: str
	phone: str
	created_at: datetime
	status_history: NotRequired[list[dict]]
	is_active: bool


class UpdateUserData(TypedDict, total=False):
	phone: str
	is_active: bool
