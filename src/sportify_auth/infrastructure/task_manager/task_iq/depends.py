from typing import Annotated, AsyncIterable, Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from taskiq import TaskiqDepends

from sportify_auth.application.protocols.repositories import IOutboxRepository
from sportify_auth.application.services.outbox_service_impl import OutboxService
from sportify_auth.infrastructure.cache.redis import RedisCache, get_redis
from sportify_auth.infrastructure.db.sqlalchemy.db_helper import (
	create_async_session_factory,
	create_engine,
)
from sportify_auth.infrastructure.db.sqlalchemy.repositories import (
	SQLAlchemyOutboxRepository,
)
from sportify_auth.infrastructure.file_storage.jwk_storage import (
	JWKStorage,
	get_jwk_storage,
)
from sportify_auth.infrastructure.message_broker.kafka import (
	KafkaMessageProducer,
	get_producer,
)


def new_async_session_maker() -> Callable[[], async_sessionmaker[AsyncSession]]:
	engine = create_engine()
	return create_async_session_factory(engine)


def new_cache_service() -> RedisCache:
	return get_redis()


def new_file_storage() -> JWKStorage:
	return get_jwk_storage()


def new_message_producer() -> KafkaMessageProducer:
	return get_producer()


async def new_session(
	session_maker: Annotated[
		async_sessionmaker[AsyncSession],
		TaskiqDepends(new_async_session_maker),
	],
) -> AsyncIterable[AsyncSession]:
	async with session_maker() as session:
		yield session


def new_outbox_repository(
	session: Annotated[AsyncSession, TaskiqDepends(new_session)],
) -> SQLAlchemyOutboxRepository:
	return SQLAlchemyOutboxRepository(session)


def new_outbox_service(
	outbox_repository: Annotated[IOutboxRepository, TaskiqDepends(new_outbox_repository)],
) -> OutboxService:
	return OutboxService(outbox_repository)
