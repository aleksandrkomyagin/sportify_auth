from fastapi import APIRouter

from .service import service_router
from .session import session_router
from .token import token_router
from .user import user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user_router)
v1_router.include_router(token_router)
v1_router.include_router(service_router)
v1_router.include_router(session_router)
