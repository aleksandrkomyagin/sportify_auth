from fastapi import APIRouter

from .generate_new_jwks import jwks_router
from .health import health_router

service_router = APIRouter(prefix="/service", tags=["service"])

service_router.include_router(jwks_router)
service_router.include_router(health_router)
