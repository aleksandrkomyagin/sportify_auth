from logging import getLogger

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from sportify_auth.application.common.exceptions.base import (
	BaseAppException,
	BaseDetailException,
)
from sportify_auth.infrastructure.common.exceptions.base import (
	BaseInfraException,
	BaseServiceAuthException,
)

logger = getLogger(__name__)


def register_exception_handler(app: FastAPI):
	@app.exception_handler(BaseServiceAuthException)
	async def auth_exception_handler(request: Request, exc: BaseServiceAuthException):
		return JSONResponse(
			{"message": exc.message},
			status_code=status.HTTP_401_UNAUTHORIZED,
		)

	@app.exception_handler(BaseAppException)
	async def app_exception_handler(request: Request, exc: BaseDetailException):
		if isinstance(exc.__cause__, BaseInfraException):
			exc.response_data["detail"]["text"] = "Внутренняя ошибка сервера"
			return JSONResponse(
				exc.response_data, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
		return JSONResponse(exc.response_data, status_code=exc.status_code)

	@app.exception_handler(Exception)
	async def unhandled_exception_handler(request: Request, exc: Exception):
		return JSONResponse(
			{"message": "Внутренняя ошибка сервера"},
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		)
