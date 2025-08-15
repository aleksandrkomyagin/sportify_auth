from functools import lru_cache
from logging import getLogger
from taskiq_redis import RedisScheduleSource, RedisStreamBroker

from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from sportify_auth.infrastructure.task_manager.task_iq.task_manager import TaskManager
from sportify_auth.setup.config import settings


logger = getLogger(__name__)


@lru_cache
def get_task_manager() -> TaskManager:
    broker = RedisStreamBroker(settings.redis.url + settings.redis.tasks_db)
    source = RedisScheduleSource(settings.redis.url + settings.redis.tasks_db)
    scheduler = TaskiqScheduler(broker, [LabelScheduleSource(broker), source])
    return TaskManager(broker, source, scheduler)
