from functools import lru_cache

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
	AsyncEngine,
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)

from sportify_auth.infrastructure.exceptions.db.sql_alchemy import StartEngineException
from sportify_auth.setup.config import settings


@lru_cache
def create_engine() -> AsyncEngine:
	try:
		engine = create_async_engine(settings.postgres.connection_string())
	except SQLAlchemyError as e:
		raise StartEngineException(message="Ошибка при старте движка БД") from e
	return engine


def create_async_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
	return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
