from contextlib import asynccontextmanager
from logging import config, getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sportify_auth.infrastructure.cache.redis import get_redis
from sportify_auth.infrastructure.message_broker.kafka import get_consumer, get_producer
from sportify_auth.infrastructure.task_manager.task_iq.factory import get_task_manager
from sportify_auth.presentation import main_api_router
from sportify_auth.presentation.exception_handlers import register_exception_handler
from sportify_auth.presentation.middlewares.request_id_middleware import (
	RequestIDMiddleware,
)
from sportify_auth.setup.config import APIConfig, settings
from sportify_auth.setup.di import dependencies, dependency_container
from sportify_auth.setup.gunicorn import ApplicationServer, get_options
from sportify_auth.setup.logger import get_log_config

config.dictConfig(get_log_config())
logger = getLogger(__name__)


async def start_task_manager(app: FastAPI):
	tm = get_task_manager()
	await tm.start()
	app.state.task_manager = tm


async def start_kafka_producer(app: FastAPI):
	producer = get_producer()
	await producer.start()
	app.state.producer = producer


async def start_kafka_consumer(app: FastAPI):
	engine = dependencies.new_engine()
	broker_async_sessionmaker = dependencies.new_async_session_maker(engine)
	consumer = get_consumer()
	await consumer.start(broker_async_sessionmaker)
	app.state.consumer = consumer


def setup_dependencies(app: FastAPI):
	app.dependency_overrides.update(dependency_container)


def setup_routers(app: FastAPI):
	app.include_router(main_api_router)


def setup_middlewares(app: FastAPI):
	app.add_middleware(
		CORSMiddleware,
		allow_origins=settings.api_config.cors_origins.split(","),
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
	app.add_middleware(RequestIDMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
	await start_kafka_producer(app)
	await start_kafka_consumer(app)
	await start_task_manager(app)
	yield
	await app.state.consumer.stop()
	await app.state.producer.stop()
	await app.state.task_manager.stop()
	await get_redis().close_connection()


def init_app(debug: bool = False) -> FastAPI:
	app = FastAPI(debug=debug, title="Sportify Auth service", version="1.0.0", lifespan=lifespan)
	setup_dependencies(app)
	setup_routers(app)
	register_exception_handler(app)
	setup_middlewares(app)

	return app


def run_app(app: FastAPI, api_config: APIConfig) -> None:
	ApplicationServer(
		app,
		options=get_options(
			api_config.host,
			int(api_config.port),
			api_config.workers,
			get_log_config(),
		),
	).run()
