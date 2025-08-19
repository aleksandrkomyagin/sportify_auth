from logging import getLogger
from typing import Annotated

from aiokafka.errors import KafkaError
from taskiq import TaskiqDepends

from sportify_auth.application.protocols.cache import ICacheService
from sportify_auth.application.protocols.file_storages.base import IJWKStorage
from sportify_auth.application.protocols.message_broker import IMessageProducer
from sportify_auth.application.protocols.services import IOutboxService
from sportify_auth.infrastructure.task_manager.task_iq.depends import (
	new_cache_service,
	new_file_storage,
	new_message_producer,
	new_outbox_service,
)
from sportify_auth.infrastructure.task_manager.task_iq.factory import get_task_manager
from sportify_auth.setup.config import settings

task_manager = get_task_manager()
logger = getLogger(__name__)


@task_manager.broker.task("delete_expired_jwk")
async def delete_expired_jwk(
	kid: str | None,
	cache: Annotated[ICacheService, TaskiqDepends(new_cache_service)],
	file_storage: Annotated[IJWKStorage, TaskiqDepends(new_file_storage)],
):
	if kid:
		logger.info("Старт задачи для удаления устаревшего KID: %s", kid)
		jwks = await cache.get(settings.redis.jwks_db, "JWKS")
		filtered_jwks = list(filter(lambda jwk: jwk["kid"] != kid, jwks))
		await cache.set(
			settings.redis.jwks_db,
			"JWKS",
			filtered_jwks,
		)
		await file_storage.replace(filtered_jwks)


@task_manager.broker.task("outbox_task", schedule=[{"cron": "* * * * *"}])
async def process_outbox(
	outbox_service: Annotated[IOutboxService, TaskiqDepends(new_outbox_service)],
	producer: Annotated[IMessageProducer, TaskiqDepends(new_message_producer)],
):
	logger.info("Старт outbox задачи")
	events = await outbox_service.get_not_processed_events()
	logger.info("К обработке %s событий", len(events))

	sent_event_ids = []
	not_sent_event_ids = []

	for event in events:
		try:
			await producer.send_and_wait(event.topic, event.payload)
		except (Exception, KafkaError) as e:
			logger.error("Ошибка при отправке события в кафку %s", str(e), exc_info=True)
			not_sent_event_ids.append(event.id)
		sent_event_ids.append(event.id)

	await outbox_service.change_event_statuses(sent_event_ids, status="processed")
	await outbox_service.change_event_statuses(not_sent_event_ids, status="not_processed")
