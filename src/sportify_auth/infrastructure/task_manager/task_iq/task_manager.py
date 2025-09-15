from datetime import datetime, timedelta, timezone
from logging import getLogger

from taskiq import TaskiqScheduler
from taskiq_redis import RedisScheduleSource, RedisStreamBroker

from sportify_auth.application.protocols.task_manager.base import ITaskManager

logger = getLogger(__name__)


class TaskManager(ITaskManager):
	def __init__(
		self,
		broker: RedisStreamBroker,
		source: RedisScheduleSource,
		scheduler: TaskiqScheduler,
	):
		self.broker = broker
		self.scheduler = scheduler
		self._source = source

	async def start(self):
		if not self.broker.is_worker_process:
			await self.broker.startup()

	async def stop(self):
		if not self.broker.is_worker_process:
			await self.broker.shutdown()

	async def delay_by_time(self, task_name: str, *args) -> None:
		task = self.broker.local_task_registry.get(task_name)
		if task is None:
			return
		eta = datetime.now(timezone.utc) + timedelta(days=1)
		await task.schedule_by_time(self._source, eta, *args)
