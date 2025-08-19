from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware

from sportify_auth.infrastructure.context.request_id import request_id_var


class RequestIDMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request, call_next):
		request_id = request.headers.get("X-Request-ID", str(uuid4()))
		request_id_var.set(request_id)
		response = await call_next(request)
		response.headers["X-Request-ID"] = request_id
		return response
