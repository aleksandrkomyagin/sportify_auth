from logging import getLogger

from taskiq import TaskiqEvents, TaskiqState
from sportify_auth.infrastructure.message_broker.kafka import get_producer
from sportify_auth.infrastructure.task_manager.task_iq.factory import get_task_manager

tm = get_task_manager()
logger = getLogger(__name__)



@tm.broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_startup(state: TaskiqState):
    producer = get_producer()
    await producer.start()

@tm.broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def on_shutdown(state: TaskiqState):
    producer = get_producer()
    await producer.stop()
