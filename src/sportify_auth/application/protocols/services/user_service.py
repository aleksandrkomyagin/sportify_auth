from abc import abstractmethod
from typing import Protocol

from sportify_auth.application.dto.event import NewOutboxEventDTO
from sportify_auth.application.dto.user import (
	UserIdDTO,
	UserSignInConfirmRequest,
	UserSignUpConfirmRequest,
)
from sportify_auth.application.schemas.requests import (
	UserActivateConfirmRequestSchema,
	UserActivateRequestSchema,
	UserDeactivateRequestSchema,
	UserDeleteRequestSchema,
	UserSignInRequestSchema,
	UserSignUpRequestSchema,
)


class IUserService(Protocol):
	@abstractmethod
	async def signup_confirm(
		self, user_data: UserSignUpConfirmRequest
	) -> tuple[NewOutboxEventDTO, UserIdDTO]:
		pass

	@abstractmethod
	async def signup(self, user_data: UserSignUpRequestSchema) -> UserIdDTO:
		pass

	@abstractmethod
	async def signin(self, user_data: UserSignInRequestSchema) -> UserIdDTO:
		pass

	@abstractmethod
	async def signin_confirm(self, user_data: UserSignInConfirmRequest) -> UserIdDTO:
		pass

	@abstractmethod
	async def user_activate(self, user_data: UserActivateRequestSchema) -> UserIdDTO:
		pass

	@abstractmethod
	async def user_activate_confirm(
		self, user_data: UserActivateConfirmRequestSchema
	) -> tuple[NewOutboxEventDTO, UserIdDTO]:
		pass

	@abstractmethod
	async def user_deactivate(
		self, user_data: UserDeactivateRequestSchema
	) -> tuple[NewOutboxEventDTO, UserIdDTO]:
		pass

	@abstractmethod
	async def delete_user(
		self, user_data: UserDeleteRequestSchema
	) -> tuple[NewOutboxEventDTO, UserIdDTO]:
		pass
