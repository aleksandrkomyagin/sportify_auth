from . import lifecycle, tasks
from .factory import get_task_manager

task_manager = get_task_manager()

broker = task_manager.broker
scheduler = task_manager.scheduler

__all__ = (
	"broker",
	"scheduler",
	"tasks",
	"lifecycle",
)
