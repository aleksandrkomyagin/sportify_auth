from datetime import datetime

from sportify_auth.application.protocols.repositories.user.types import (
	UpdateUserData,
	UserData,
)
from sportify_auth.domain.entities import User
from sportify_auth.domain.value_objects import IsActive, Phone, UserUUID


class UserMapper:
	@staticmethod
	def to_dict(user: User) -> UserData:
		return {
			"id": user.id.value,
			"phone": user.phone.value,
			"is_active": user.is_active.value,
			"created_at": user.created_at,
			"status_history": [
				{
					"user_id": item.user_id.value,
					"status": item.status,
					"timestamp": item.timestamp,
				}
				for item in user.status_history
			],
		}

	@staticmethod
	def from_dict(data: dict) -> User:
		return User(
			id=UserUUID(data["id"]),
			phone=Phone(data["phone"]),
			is_active=IsActive(data["is_active"]),
			created_at=datetime.fromisoformat(data["created_at"]),
		)

	@staticmethod
	def to_cache(user: User) -> dict:
		return {
			"id": user.id.value,
			"phone": user.phone.value,
			"is_active": user.is_active.value,
			"created_at": user.created_at.isoformat(),
		}

	@staticmethod
	def to_update(user: dict) -> UpdateUserData:
		return UpdateUserData(**user)
