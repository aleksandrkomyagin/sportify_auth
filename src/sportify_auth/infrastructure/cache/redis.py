import json

from functools import lru_cache
from logging import getLogger
from typing import Any

from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import RedisError

from sportify_auth.application.protocols.cache import ICacheService
from sportify_auth.infrastructure.exceptions.cache.redis import (
	RedisConnectionException,
	RedisOperationException,
)
from sportify_auth.setup.config import settings

logger = getLogger(__name__)


class RedisCache(ICacheService):
	def __init__(self, redis_url: str):
		self.redis_url = redis_url
		self.instances: dict[str, Redis] = dict()

	def get_instance(self, db_name: str) -> Redis:
		if db_name not in self.instances:
			try:
				pool = ConnectionPool().from_url(
					f"{self.redis_url}/{db_name}",
					decode_responses=True,
				)
				self.instances[db_name] = Redis.from_pool(pool)
			except RedisError as e:
				logger.error("Ошибка получения инстанса: %s", str(e))
				raise RedisConnectionException(message="Ошибка получения инстанса") from e
		return self.instances[db_name]

	async def set(self, db_name: str, key: str, value: Any, expire: int | None = None) -> None:
		redis = self.get_instance(db_name)
		try:
			if not isinstance(value, str):
				value = json.dumps(value)
			await redis.set(key, value, ex=expire)
		except Exception as e:
			logger.error("Ошибка записи: %s", str(e))
			raise RedisOperationException(message="Ошибка записи в редис") from e

	async def append(
		self,
		db_name: str,
		key: str,
		value: Any,
	) -> None:
		redis = self.get_instance(db_name)
		data_set = await redis.get(key)
		try:
			data_set = json.loads(data_set) if data_set else []
			data_set.append(value)
			value = json.dumps(data_set)
			await redis.set(key, value)
		except Exception as e:
			logger.error("Ошибка добавления по ключу: %s", str(e))
			raise RedisOperationException(message="Ошибка добавления по ключу в редис") from e

	async def get(self, db_name: str, key: str) -> Any | None:
		redis = self.get_instance(db_name)
		try:
			value = await redis.get(key)
			if value:
				try:
					return json.loads(value)
				except json.JSONDecodeError:
					return value
			return None
		except Exception as e:
			logger.error("Ошибка чтения по ключу: %s", str(e))
			raise RedisOperationException(message="Ошибка чтения по ключу из редис") from e

	async def delete(self, db_name: str, key: str) -> None:
		redis = self.get_instance(db_name)
		try:
			await redis.delete(key)
		except Exception as e:
			logger.error("Ошибка удаления по ключу: %s", str(e))
			raise RedisOperationException(message="Ошибка удаления по ключу из редис") from e

	async def exists(self, db_name: str, key: str) -> bool:
		redis = self.get_instance(db_name)
		return await redis.exists(key) > 0

	async def keys(self, db_name: str, pattern: str = "*") -> list[str]:
		redis = self.get_instance(db_name)
		return await redis.keys(pattern)

	async def close_connection(self) -> None:
		for redis in self.instances.values():
			await redis.connection_pool.disconnect()

	async def flush_db(self, db_name: str) -> None:
		redis = self.get_instance(db_name)
		await redis.flushdb()


@lru_cache
def get_redis() -> RedisCache:
	return RedisCache(settings.redis.url)
