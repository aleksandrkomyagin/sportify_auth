import sys
from logging import getLogger

from sportify_auth.setup.app_factory import init_app, run_app
from sportify_auth.setup.config import settings

logger = getLogger(__name__)


def start():
	try:
		app = init_app(settings.api_config.debug)
	except Exception as e:
		logger.error("Ошибка при инициализации сервера: %s", str(e), exc_info=True)
		sys.exit(1)
	run_app(app, settings.api_config)


if __name__ == "__main__":
	start()
