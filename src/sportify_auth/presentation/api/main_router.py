from fastapi import APIRouter

from .v1 import v1_router

main_api_router = APIRouter(prefix="/api")

main_api_router.include_router(v1_router)
