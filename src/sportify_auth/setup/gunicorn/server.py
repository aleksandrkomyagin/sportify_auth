from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class ApplicationServer(BaseApplication):
    def __init__(self, application: FastAPI, options: dict):
        self.application = application
        self.options = options
        super(ApplicationServer, self).__init__()

    def load(self):
        return self.application

    def _config_options(self) -> dict:
        return {
            k: v
            for k, v in self.options.items()
            if k in self.cfg.settings and v is not None
        }

    def load_config(self):
        for key, value in self._config_options().items():
            self.cfg.set(key.lower(), value)
