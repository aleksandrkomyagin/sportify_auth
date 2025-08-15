from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserSignInRequestSchema
from sportify_auth.application.schemas.responses import UserSignInResponseSchema
from sportify_auth.application.interactors.user import UserSignInInteractor

signin_router = APIRouter()


@signin_router.post("/signin", response_model=UserSignInResponseSchema)
async def signin(
	request_data: UserSignInRequestSchema,
	interactor: Annotated[UserSignInInteractor, Depends(Stub(UserSignInInteractor))],
):
	return await interactor(request_data)
