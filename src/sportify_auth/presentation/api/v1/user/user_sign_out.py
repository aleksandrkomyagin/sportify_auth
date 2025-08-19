from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.interactors.user import UserSignOutInteractor
from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserSignOutRequestSchema
from sportify_auth.application.schemas.responses import UserSignOutResponseSchema
from sportify_auth.presentation.auth import authenticate

sign_out_router = APIRouter(dependencies=[Depends(authenticate)])


@sign_out_router.post("/signout", response_model=UserSignOutResponseSchema)
async def sign_out(
	request_data: UserSignOutRequestSchema,
	interactor: Annotated[UserSignOutInteractor, Depends(Stub(UserSignOutInteractor))],
):
	return await interactor(request_data)
