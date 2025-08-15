from fastapi import APIRouter

from .refresh_token import refresh_router
from .revoke_token import revoke_router

token_router = APIRouter(prefix="/token", tags=["token"])

token_router.include_router(refresh_router)
token_router.include_router(revoke_router)
