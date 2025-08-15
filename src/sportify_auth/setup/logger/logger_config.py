from sportify_auth.setup.config import settings


def get_log_config():
	handlers = ["default"] if settings.api_config.debug else ["json"]
	return {
		"version": 1,
		"disable_existing_loggers": False,
		"filters": {
			"request_id_filter": {
				"()": "sportify_auth.setup.logger.RequestIdFilter",
			}
		},
		"formatters": {
			"default": {
				"()": "sportify_auth.setup.logger.DateTimeFormatter",
				"fmt": "[%(asctime)-15s] [%(levelname)-7s] %(message)s module=%(module)s request_id=%(request_id)s",
			},
			"json": {
				"()": "sportify_auth.setup.logger.JsonFormatter",
			}
		},
		"handlers": {
			"default": {
				"level": "DEBUG",
				"formatter": "default",
				"class": "logging.StreamHandler",
				"filters": ["request_id_filter"],
			},
			"json": {
				"level": "DEBUG",
				"formatter": "json",
				"class": "sportify_auth.setup.logger.JSONHandler",
				"filters": ["request_id_filter"],
			}
		},
		"loggers": {
			"gunicorn.error": {
				"handlers": ["default"],
				"level": settings.api_config.log_level.upper(),
				"propagate": False
			},
			"gunicorn.access": {
				"handlers": ["default"],
				"level": settings.api_config.log_level.upper(),
				"propagate": False,
			},
		},
		"root": {
			"level": settings.api_config.log_level.upper(),
			"handlers": handlers
		},
	}
