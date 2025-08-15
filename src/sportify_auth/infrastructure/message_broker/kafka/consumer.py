import asyncio
import json
from functools import lru_cache
from logging import getLogger
from typing import Any, Callable

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sportify_auth.application.protocols.message_broker import IMessageConsumer
from sportify_auth.infrastructure.db.sqlalchemy.repositories import SQLAlchemyUserRepository
from sportify_auth.infrastructure.exceptions.message_broker.kafka import (
	StartConsumerException,
	StopConsumerException,
)
from sportify_auth.setup.config import settings

logger = getLogger(__name__)


class KafkaMessageConsumer(IMessageConsumer):
	def __init__(self, topics: str, server: str):
		self._topics = topics
		self._server = server
		self._session_maker: async_sessionmaker[AsyncSession] | None = None
		self._consumer: AIOKafkaConsumer | None = None
		self._task: asyncio.Task | None = None
		self.handlers_registry = dict()
		self._stopped = asyncio.Event()

	@staticmethod
	def deserializer(serialized):
		return json.loads(serialized)

	def subscriber(self, topic: str):
		def decorator(func: Callable[[str], Any]):
			self.handlers_registry[topic] = func
			return func

		return decorator

	async def start(self, session_maker: async_sessionmaker[AsyncSession]):
		try:
			self._session_maker = session_maker
			self._consumer = AIOKafkaConsumer(
				bootstrap_servers=self._server,
				group_id="auth_service",
				auto_offset_reset="earliest",
				enable_auto_commit=False,
				value_deserializer=self.deserializer,
			)
			await self._consumer.start()
			self._consumer.subscribe(topics=self._topics.split(","))
			self._stopped.clear()
			self._task = asyncio.create_task(self._consume_loop())
		except KafkaError as e:
			logger.error("Ошибка при старте консюмера: %s", str(e))
			await self._consumer.stop()
			raise StartConsumerException(
				message="Ошибка при старте консюмера"
			) from e

	async def stop(self):
		try:
			self._stopped.set()
			if self._task:
				await self._task
			if self._consumer:
				await self._consumer.stop()
		except KafkaError as e:
			logger.error("Ошибка при остановке консюмера: %s", str(e))
			raise StopConsumerException(
				message="Ошибка при остановке консюмера"
			) from e

	async def _consume_loop(self):
		try:
			while not self._stopped.is_set():
				msg_batch = await self._consumer.getmany(timeout_ms=50000)
				if msg_batch:
					for tp, messages in msg_batch.items():
						handler = self.handlers_registry.get(tp.topic)
						if handler:
							for msg in messages:
								async with self._session_maker() as session:
									repo = SQLAlchemyUserRepository(session)
									try:
										await handler(msg.value, repo)
										await session.commit()
									except KafkaError as e:
										logger.error(
											"Во время обработки сообщения (offset: %s) произошла ошибка: %s",
											msg.offset,
											str(e)
										)
								await asyncio.sleep(0.5)
						else:
							logger.info("Нет обработчика для %s", tp.topic)
						await self._consumer.commit({tp: messages[-1].offset + 1})
		except KafkaError as e:
			logger.error(
				"Во время работы консьюмера произошла ошибка: %s", e, exc_info=True
			)
			logger.warning("Перезапуск консьюмера через 5 секунд")
			await self.stop()
			await asyncio.sleep(5)
			await self.start(session_maker=self._session_maker)



@lru_cache
def get_consumer():
	return KafkaMessageConsumer(settings.kafka.consumer_topics, settings.kafka.server)
