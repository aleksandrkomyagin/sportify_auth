from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

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
from sportify_auth.application.protocols.security.auth import IAuthenticateService
from sportify_auth.application.protocols.services import (
	IConfirmationCodeService,
	IOutboxService,
	ISessionService,
	ITokenService,
	IUserService,
)
from sportify_auth.application.protocols.task_manager.base import ITaskManager
from sportify_auth.setup.di import dependencies

dependency_container = dict()

dependency_container[AsyncEngine] = dependencies.new_engine
dependency_container[async_sessionmaker[AsyncSession]] = dependencies.new_async_session_maker
dependency_container[AsyncSession] = dependencies.new_session
dependency_container[IUserRepository] = dependencies.new_user_repository
dependency_container[IOutboxRepository] = dependencies.new_outbox_repository
dependency_container[ISessionRepository] = dependencies.new_session_repository
dependency_container[ITransactionManager] = dependencies.new_transaction_manager
dependency_container[IMessageProducer] = dependencies.new_message_producer
dependency_container[ICacheService] = dependencies.new_cache_service
dependency_container[IJWKStorage] = dependencies.new_file_storage
dependency_container[IKeyGenerator] = dependencies.new_rsa_key_generator
dependency_container[IConfirmationCodeService] = dependencies.new_confirmation_code_service
dependency_container[IOutboxService] = dependencies.new_outbox_service
dependency_container[ISessionService] = dependencies.new_session_service
dependency_container[ITokenService] = dependencies.new_token_service
dependency_container[IUserService] = dependencies.new_user_service
dependency_container[ITaskManager] = dependencies.new_task_manager
dependency_container[UserDeleteInteractor] = dependencies.new_user_delete_interactor
dependency_container[UserSignInConfirmInteractor] = dependencies.new_user_signin_confirm_interactor
dependency_container[UserSignInInteractor] = dependencies.new_user_signin_interactor
dependency_container[UserSignUpConfirmInteractor] = dependencies.new_user_signup_confirm_interactor
dependency_container[UserSignUpInteractor] = dependencies.new_user_signup_interactor
dependency_container[UserActivateInteractor] = dependencies.new_user_activate_interactor
dependency_container[UserActivateConfirmInteractor] = (
	dependencies.new_user_activate_confirm_interactor
)
dependency_container[UserDeactivateInteractor] = dependencies.new_user_deactivate_interactor
dependency_container[UserSignOutInteractor] = dependencies.new_user_sign_out_interactor
dependency_container[GenerateNewJWKSInteractor] = dependencies.new_generate_jwks_interactor
dependency_container[RefreshTokenInteractor] = dependencies.new_refresh_token_interactor
dependency_container[RevokeTokenInteractor] = dependencies.new_revoke_token_interactor
dependency_container[IAuthenticateService] = dependencies.new_authentication_provider
