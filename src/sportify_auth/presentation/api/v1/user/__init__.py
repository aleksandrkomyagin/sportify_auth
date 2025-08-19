from fastapi import APIRouter

from .user_activate import activate_router
from .user_activate_confirm import activate_confirm_router
from .user_deactivate import deactivate_router
from .user_delete import delete_router
from .user_sign_out import sign_out_router
from .user_signin import signin_router
from .user_signin_confirm import signin_confirm_router
from .user_signup import signup_router
from .user_signup_confirm import signup_confirm_router

user_router = APIRouter(prefix="/users", tags=["users"])

user_router.include_router(delete_router)
user_router.include_router(signin_router)
user_router.include_router(signin_confirm_router)
user_router.include_router(signup_confirm_router)
user_router.include_router(signup_router)
user_router.include_router(activate_router)
user_router.include_router(activate_confirm_router)
user_router.include_router(deactivate_router)
user_router.include_router(sign_out_router)
