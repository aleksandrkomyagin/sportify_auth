from fastapi import APIRouter

from .last_activity_update import last_activity_update_router

session_router = APIRouter(prefix="/sessions", tags=["sessions"])

session_router.include_router(last_activity_update_router)
