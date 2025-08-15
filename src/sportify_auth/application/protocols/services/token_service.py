from abc import abstractmethod
from typing import Protocol

from sportify_auth.application.dto.event import NewOutboxEventDTO
from sportify_auth.application.dto.token import TokenDTO
from sportify_auth.application.dto.user import UserIdDTO
from sportify_auth.application.schemas.requests import RefreshTokenRequestSchema, RevokeTokenRequestSchema


class ITokenService(Protocol):
	@abstractmethod
	async def generate_new_rsa_key(self) -> str:
		pass

	@abstractmethod
	async def create_token(self, user_id: UserIdDTO) -> TokenDTO:
		pass

	@abstractmethod
	async def revoke_token(self, token_payload: RevokeTokenRequestSchema) -> NewOutboxEventDTO:
		pass

	@abstractmethod
	async def refresh_token(self, token_data: RefreshTokenRequestSchema) -> TokenDTO:
		pass
