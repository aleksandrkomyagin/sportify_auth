from abc import abstractmethod
from typing import Protocol

from sportify_auth.application.protocols.repositories.user.types import UpdateUserData, UserData
from sportify_auth.domain.entities import User
from sportify_auth.domain.value_objects import UserUUID


class IUserRepository(Protocol):
	@abstractmethod
	async def create_user(self, user_data: UserData) -> UserUUID:
		raise NotImplementedError

	@abstractmethod
	async def delete_user(self, user_id: str) -> None:
		raise NotImplementedError

	@abstractmethod
	async def get_user_by_id(self, user_id: str) -> User | None:
		raise NotImplementedError

	@abstractmethod
	async def get_user_by_phone(self, phone: str) -> User | None:
		raise NotImplementedError

	@abstractmethod
	async def update_user(
		self,
		user_id: str,
		user_data: UpdateUserData,
		status_history: list[dict] | None = None
	) -> UserUUID:
		raise NotImplementedError
