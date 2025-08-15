from .factory import get_task_manager
from . import tasks
from . import lifecycle

task_manager = get_task_manager()

broker = task_manager.broker
scheduler = task_manager.scheduler

__all__ = (
    "broker",
    "scheduler",
    "tasks",
    "lifecycle",
)
