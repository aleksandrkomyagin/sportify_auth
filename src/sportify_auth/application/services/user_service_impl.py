from logging import getLogger

from sportify_auth.adapters.mappers.user_mapper import UserMapper
from sportify_auth.application.dto.user import UserIdDTO
from sportify_auth.application.dto.event import NewOutboxEventDTO
from sportify_auth.application.exceptions.user import (
	UserNotFoundException,
	UserSignupSessionHasExpiredException,
)
from sportify_auth.application.protocols.cache import ICacheService
from sportify_auth.application.protocols.message_broker import IMessageProducer
from sportify_auth.application.protocols.repositories import IUserRepository
from sportify_auth.application.protocols.services import IConfirmationCodeService, IUserService
from sportify_auth.application.schemas.requests import (
	UserActivateConfirmRequestSchema,
	UserActivateRequestSchema,
	UserDeactivateRequestSchema,
	UserDeleteRequestSchema,
	UserSignInConfirmRequestSchema,
	UserSignInRequestSchema,
	UserSignUpConfirmRequestSchema,
	UserSignUpRequestSchema,
)
from sportify_auth.domain.entities import User
from sportify_auth.setup.config import settings

logger = getLogger(__name__)


class UserService(IUserService):
	def __init__(
		self,
		user_repository: IUserRepository,
		cache: ICacheService,
		confirmation_code_service: IConfirmationCodeService,
		producer: IMessageProducer,
	) -> None:
		self._user_repository = user_repository
		self._cache = cache
		self._confirmation_code_service = confirmation_code_service
		self._producer = producer

	async def _send_confirmation_code(self, key_prefix: str, phone: str) -> None:
		code = await self._confirmation_code_service.get_code(key_prefix, phone)
		logger.info("Код подтверждения: %s", code)		# Временно, пока нет сервиса нотификации
		await self._producer.send(
			topic="notify_user", message={"phone": phone, "code": code}
		)

	async def _validate_confirmation_code(
		self, key_prefix: str, phone: str, expected_code: str
	) -> None:
		await self._confirmation_code_service.validate_code(
			key_prefix, phone, expected_code
		)

	async def user_activate(self, user_data: UserActivateRequestSchema) -> UserIdDTO:
		user = await self._user_repository.get_user_by_phone(user_data.phone)
		if not user:
			raise UserNotFoundException(message="Пользователь не найден")
		await self._send_confirmation_code("activation:code", user.phone.value)

		return UserIdDTO(user.id.value)

	async def user_activate_confirm(
		self, user_data: UserActivateConfirmRequestSchema
	) -> tuple[NewOutboxEventDTO, UserIdDTO]:
		user = await self._user_repository.get_user_by_phone(user_data.phone)
		if not user:
			raise UserNotFoundException(message="Пользователь не найден")
		await self._validate_confirmation_code(
			"activation:code", user_data.phone, user_data.code
		)
		user = user.activate()
		status_history = user.get_status_history()
		await self._user_repository.update_user(
			user.id.value,
			{"is_active": True},
			status_history=status_history
		)

		return (
			NewOutboxEventDTO(
				topic="activate_user",
				payload={"id": user.id.value, "is_active": True}
			),
			UserIdDTO(user.id.value)
		)

	async def user_deactivate(
		self, user_data: UserDeactivateRequestSchema
	) -> tuple[NewOutboxEventDTO, UserIdDTO]:
		user = await self._user_repository.get_user_by_id(user_data.user_id)
		if not user:
			raise UserNotFoundException(message="Пользователь не найден")
		user = user.deactivate()
		status_history = user.get_status_history()
		await self._user_repository.update_user(
			user.id.value, {"is_active": False}, status_history=status_history
		)

		return (
			NewOutboxEventDTO(
				topic="deactivate_user",
				payload={"id": user.id.value, "is_active": False}
			),
			UserIdDTO(user.id.value)
		)

	async def signup_confirm(
		self, user_data: UserSignUpConfirmRequestSchema
	) -> tuple[NewOutboxEventDTO, UserIdDTO]:
		cached_user = await self._cache.get(
			settings.redis.user_db, f"signup:user:{user_data.phone}"
		)
		if not cached_user:
			raise UserSignupSessionHasExpiredException(
				message="Время сессии регистрации истекло, пожалуйста, начните заново",
			)
		await self._validate_confirmation_code(
			"signup:code", user_data.phone, user_data.code
		)
		user = UserMapper.from_dict(cached_user)
		user = user.confirm_signup()
		user_id = await self._user_repository.create_user(UserMapper.to_dict(user))

		return (
			NewOutboxEventDTO(
				topic="create_user",
				payload={"id": user.id.value, "phone": user.phone.value}
			),
			UserIdDTO(user_id.value)
		)

	async def signup(self, user_data: UserSignUpRequestSchema) -> UserIdDTO:
		existing_user = await self._user_repository.get_user_by_phone(user_data.phone)
		user = User.signup(user_data.phone, existing_user)
		await self._cache.set(
			settings.redis.user_db,
			f"signup:user:{user.phone.value}",
			UserMapper.to_cache(user),
			6000,
		)
		await self._send_confirmation_code("signup:code", user.phone.value)

		return UserIdDTO(user.id.value)

	async def signin(self, user_data: UserSignInRequestSchema) -> UserIdDTO:
		user = await self._user_repository.get_user_by_phone(user_data.phone)
		if not user:
			raise UserNotFoundException(message="Пользователь не найден")
		user.can_login()
		await self._send_confirmation_code("signin:code", user.phone.value)

		return UserIdDTO(user.id.value)

	async def signin_confirm(
		self, user_data: UserSignInConfirmRequestSchema
	) -> UserIdDTO:
		user = await self._user_repository.get_user_by_phone(user_data.phone)
		if not user:
			raise UserNotFoundException(message="Пользователь не найден")
		await self._validate_confirmation_code(
			"signin:code", user_data.phone, user_data.code
		)

		return UserIdDTO(user.id.value)

	async def delete_user(
		self, user_data: UserDeleteRequestSchema
	) -> tuple[NewOutboxEventDTO, UserIdDTO]:
		user = await self._user_repository.get_user_by_id(user_data.user_id)
		if not user:
			raise UserNotFoundException(message="Пользователь не найден")
		await self._user_repository.delete_user(user.id.value)

		return (
			NewOutboxEventDTO(
				topic="delete_user",
				payload={"id": user.id.value, "phone": user.phone.value}
			),
			UserIdDTO(user.id.value)
		)
