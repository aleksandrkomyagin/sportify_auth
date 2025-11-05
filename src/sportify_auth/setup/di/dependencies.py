from functools import lru_cache
from typing import Annotated, AsyncIterable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from sportify_auth.application.interactors.session import SessionLastActivityUpdateInteractor
from sportify_auth.application.interactors.token import (
	GenerateNewJWKSInteractor,
	RefreshTokenInteractor,
	RevokeTokenInteractor,
)
from sportify_auth.application.interactors.user import (
	UserActivateConfirmInteractor,
	UserActivateInteractor,
	UserDeactivateInteractor,
	UserDeleteInteractor,
	UserSignInConfirmInteractor,
	UserSignInInteractor,
	UserSignOutInteractor,
	UserSignUpConfirmInteractor,
	UserSignUpInteractor,
)
from sportify_auth.application.protocols.cache import ICacheService
from sportify_auth.application.protocols.file_storages.base import IJWKStorage
from sportify_auth.application.protocols.key_generator.base import IKeyGenerator
from sportify_auth.application.protocols.message_broker import IMessageProducer
from sportify_auth.application.protocols.repositories import (
	IOutboxRepository,
	ISessionRepository,
	ITransactionManager,
	IUserRepository,
)
from sportify_auth.application.protocols.services import (
	IConfirmationCodeService,
	IOutboxService,
	ISessionService,
	ITokenService,
	IUserService,
)
from sportify_auth.application.protocols.task_manager.base import ITaskManager
from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.services import (
	ConfirmationCodeService,
	SessionService,
	TokenService,
	UserService,
)
from sportify_auth.application.services.outbox_service_impl import OutboxService
from sportify_auth.infrastructure.cache.redis import RedisCache, get_redis
from sportify_auth.infrastructure.crypto.rsa_key_generator import (
	RSAKeyGenerator,
	get_rsa_key_generator,
)
from sportify_auth.infrastructure.db.sqlalchemy.db_helper import (
	create_async_session_factory,
	create_engine,
)
from sportify_auth.infrastructure.db.sqlalchemy.repositories import (
	SQLAlchemyOutboxRepository,
	SQLAlchemySessionRepository,
	SQLAlchemyUserRepository,
)
from sportify_auth.infrastructure.db.sqlalchemy.transaction_manager import (
	SqlalchemyTransactionManager,
)
from sportify_auth.infrastructure.file_storage.jwk_storage import (
	JWKStorage,
	get_jwk_storage,
)
from sportify_auth.infrastructure.message_broker.kafka import (
	KafkaMessageProducer,
	get_producer,
)
from sportify_auth.infrastructure.security.auth import AuthenticateService
from sportify_auth.infrastructure.task_manager.task_iq.factory import (
	TaskManager,
	get_task_manager,
)


def new_engine():
	return create_engine()


@lru_cache
def new_async_session_maker(
	engine: Annotated[AsyncEngine, Depends(Stub(AsyncEngine))],
) -> async_sessionmaker[AsyncSession]:
	return create_async_session_factory(engine)


async def new_session(
	session_maker: Annotated[
		async_sessionmaker[AsyncSession],
		Depends(Stub(async_sessionmaker[AsyncSession])),
	],
) -> AsyncIterable[AsyncSession]:
	async with session_maker() as session:
		yield session


def new_user_repository(
	session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> SQLAlchemyUserRepository:
	return SQLAlchemyUserRepository(session)


def new_outbox_repository(
	session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> SQLAlchemyOutboxRepository:
	return SQLAlchemyOutboxRepository(session)


def new_session_repository(
	session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> SQLAlchemySessionRepository:
	return SQLAlchemySessionRepository(session)


def new_transaction_manager(
	session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> SqlalchemyTransactionManager:
	return SqlalchemyTransactionManager(session)


def new_cache_service() -> RedisCache:
	return get_redis()


def new_file_storage() -> JWKStorage:
	return get_jwk_storage()


def new_rsa_key_generator() -> RSAKeyGenerator:
	return get_rsa_key_generator()


def new_message_producer() -> KafkaMessageProducer:
	return get_producer()


def new_confirmation_code_service(
	cache_service: Annotated[ICacheService, Depends()],
) -> ConfirmationCodeService:
	return ConfirmationCodeService(cache_service)


def new_user_service(
	user_repository: Annotated[IUserRepository, Depends()],
	cache_service: Annotated[ICacheService, Depends()],
	confirmation_code_service: Annotated[IConfirmationCodeService, Depends()],
	producer: Annotated[IMessageProducer, Depends()],
) -> UserService:
	return UserService(user_repository, cache_service, confirmation_code_service, producer)


def new_outbox_service(
	outbox_repository: Annotated[IOutboxRepository, Depends()],
) -> OutboxService:
	return OutboxService(outbox_repository)


def new_token_service(
	cache_service: Annotated[ICacheService, Depends()],
	file_storage: Annotated[IJWKStorage, Depends()],
	rsa_key_generator: Annotated[IKeyGenerator, Depends()],
) -> TokenService:
	return TokenService(cache_service, file_storage, rsa_key_generator)


def new_session_service(
	session_repository: Annotated[ISessionRepository, Depends()],
) -> SessionService:
	return SessionService(session_repository)


def new_task_manager() -> TaskManager:
	return get_task_manager()


def new_user_delete_interactor(
	user_service: Annotated[IUserService, Depends()],
	outbox_service: Annotated[IOutboxService, Depends()],
	tm: Annotated[ITransactionManager, Depends()],
) -> UserDeleteInteractor:
	return UserDeleteInteractor(user_service, outbox_service, tm)


def new_user_signin_interactor(
	user_service: Annotated[IUserService, Depends()],
) -> UserSignInInteractor:
	return UserSignInInteractor(user_service)


def new_user_signin_confirm_interactor(
	user_service: Annotated[IUserService, Depends()],
	outbox_service: Annotated[IOutboxService, Depends()],
	token_service: Annotated[ITokenService, Depends()],
	session_service: Annotated[ISessionService, Depends()],
	tm: Annotated[ITransactionManager, Depends()],
) -> UserSignInConfirmInteractor:
	return UserSignInConfirmInteractor(
		user_service, outbox_service, token_service, session_service, tm
	)


def new_user_signup_interactor(
	user_service: Annotated[IUserService, Depends()],
	tm: Annotated[ITransactionManager, Depends()],
) -> UserSignUpInteractor:
	return UserSignUpInteractor(user_service, tm)


def new_user_signup_confirm_interactor(
	user_service: Annotated[IUserService, Depends()],
	outbox_service: Annotated[IOutboxService, Depends()],
	session_service: Annotated[ISessionService, Depends()],
	token_service: Annotated[ITokenService, Depends()],
	tm: Annotated[ITransactionManager, Depends()],
) -> UserSignUpConfirmInteractor:
	return UserSignUpConfirmInteractor(
		user_service, outbox_service, session_service, token_service, tm
	)


def new_user_activate_interactor(
	user_service: Annotated[IUserService, Depends()],
) -> UserActivateInteractor:
	return UserActivateInteractor(user_service)


def new_user_activate_confirm_interactor(
	user_service: Annotated[IUserService, Depends()],
	outbox_service: Annotated[IOutboxService, Depends()],
	tm: Annotated[ITransactionManager, Depends()],
) -> UserActivateConfirmInteractor:
	return UserActivateConfirmInteractor(user_service, outbox_service, tm)


def new_user_deactivate_interactor(
	user_service: Annotated[IUserService, Depends()],
	outbox_service: Annotated[IOutboxService, Depends()],
	tm: Annotated[ITransactionManager, Depends()],
) -> UserDeactivateInteractor:
	return UserDeactivateInteractor(user_service, outbox_service, tm)


def new_user_sign_out_interactor(
	session_service: Annotated[ISessionService, Depends()],
	outbox_service: Annotated[IOutboxService, Depends()],
	tm: Annotated[ITransactionManager, Depends()],
) -> UserSignOutInteractor:
	return UserSignOutInteractor(session_service, outbox_service, tm)


def new_refresh_token_interactor(
	outbox_service: Annotated[IOutboxService, Depends()],
	token_service: Annotated[ITokenService, Depends()],
	session_service: Annotated[ISessionService, Depends()],
	tm: Annotated[ITransactionManager, Depends()],
) -> RefreshTokenInteractor:
	return RefreshTokenInteractor(outbox_service, token_service, session_service, tm)


def new_revoke_token_interactor(
	token_service: Annotated[ITokenService, Depends()],
	outbox_service: Annotated[IOutboxService, Depends()],
) -> RevokeTokenInteractor:
	return RevokeTokenInteractor(token_service, outbox_service)


def new_last_activity_update_interactor(
	session_service: Annotated[ISessionService, Depends()],
) -> SessionLastActivityUpdateInteractor:
	return SessionLastActivityUpdateInteractor(session_service)


def new_generate_jwks_interactor(
	token_service: Annotated[ITokenService, Depends()],
	task_manager: Annotated[ITaskManager, Depends()],
) -> GenerateNewJWKSInteractor:
	return GenerateNewJWKSInteractor(token_service, task_manager)


def new_authentication_provider() -> AuthenticateService:
	return AuthenticateService()
