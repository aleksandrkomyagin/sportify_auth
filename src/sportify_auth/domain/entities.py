import uuid

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from logging import getLogger
from typing import Literal, Self

from sportify_auth.domain.common.entities.base import Entity
from sportify_auth.domain.exceptions.user import (
	InactiveUserException,
	PhoneAlreadyExistsException,
)
from sportify_auth.domain.value_objects import IsActive, Phone, UserUUID

logger = getLogger(__name__)


@dataclass(frozen=True)
class UserStatusHistory:
	user_id: UserUUID
	status: Literal["activated", "deactivated"]
	timestamp: datetime


@dataclass(frozen=True)
class User(Entity):
	id: UserUUID
	phone: Phone
	created_at: datetime
	status_history: list[UserStatusHistory] = field(default_factory=list)
	is_active: IsActive = field(default_factory=lambda: IsActive(False))

	def confirm_signup(self) -> Self:
		return self.activate()

	@classmethod
	def signup(
		cls,
		phone: str,
		existing_user: Self | None,
	) -> Self:
		if existing_user:
			raise PhoneAlreadyExistsException(message="Пользователь с таким номером уже существует")

		user = cls(
			id=UserUUID(str(uuid.uuid4())),
			phone=Phone(phone),
			created_at=datetime.now(timezone.utc),
		)
		return user

	def can_login(self) -> None:
		if not self.is_active.value:
			raise InactiveUserException(message="Сначала нужно активировать профиль")

	def activate(self) -> Self:
		return replace(
			self,
			is_active=IsActive(True),
			status_history=[
				*self.status_history,
				UserStatusHistory(
					user_id=self.id,
					status="activated",
					timestamp=datetime.now(timezone.utc),
				),
			],
		)

	def deactivate(self) -> Self:
		return replace(
			self,
			is_active=IsActive(False),
			status_history=[
				*self.status_history,
				UserStatusHistory(
					user_id=self.id,
					status="deactivated",
					timestamp=datetime.now(timezone.utc),
				),
			],
		)

	def get_status_history(self) -> list[dict]:
		return [
			{
				"user_id": item.user_id.value,
				"status": item.status,
				"timestamp": item.timestamp,
			}
			for item in self.status_history
		]
