import json

from functools import lru_cache
from logging import getLogger

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from sportify_auth.application.protocols.message_broker import IMessageProducer
from sportify_auth.infrastructure.exceptions.message_broker.kafka import (
	SendMessageException,
	StartProducerException,
	StopProducerException,
)
from sportify_auth.setup.config import settings

logger = getLogger(__name__)


class KafkaMessageProducer(IMessageProducer):
	def __init__(self, server: str):
		self._server = server
		self._producer: AIOKafkaProducer = AIOKafkaProducer(
			bootstrap_servers=self._server,
			value_serializer=self.serializer,
			compression_type="gzip",
			acks="all",
		)

	@staticmethod
	def serializer(value) -> bytes:
		return json.dumps(value).encode("utf-8")

	async def send(self, topic: str, message: dict, key: str | None = None) -> None:
		try:
			await self._producer.send(topic, key=key, value=message)
			await self._producer.flush()
		except KafkaError as e:
			logger.error("Ошибка при отправке сообщения продюсером: %s", str(e))
			raise SendMessageException(message="Ошибка при отправке сообщения продюсером") from e

	async def send_and_wait(self, topic: str, message: dict, key: str | None = None) -> None:
		try:
			await self._producer.send_and_wait(topic, key=key, value=message)
		except KafkaError as e:
			logger.error("Ошибка при отправке сообщения продюсером: %s", str(e))
			raise SendMessageException(message="Ошибка при отправке сообщения продюсером") from e

	async def start(self) -> None:
		try:
			await self._producer.start()
		except KafkaError as e:
			logger.error("Ошибка при старте продюсера: %s", str(e))
			raise StartProducerException(message="Ошибка при старте продюсера") from e

	async def stop(self) -> None:
		try:
			await self._producer.stop()
		except KafkaError as e:
			logger.error("Ошибка при остановке продюсера: %s", str(e))
			raise StopProducerException(message="Ошибка при остановке продюсера") from e


@lru_cache
def get_producer():
	return KafkaMessageProducer(settings.kafka.server)
