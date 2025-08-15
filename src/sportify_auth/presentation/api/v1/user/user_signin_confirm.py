from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserSignInConfirmRequestSchema
from sportify_auth.application.schemas.responses import UserSignInConfirmResponseSchema
from sportify_auth.application.interactors.user import UserSignInConfirmInteractor

signin_confirm_router = APIRouter()


@signin_confirm_router.post(
	"/signin_confirm", response_model=UserSignInConfirmResponseSchema
)
async def signin_confirm(
	request_data: UserSignInConfirmRequestSchema,
	interactor: Annotated[
		UserSignInConfirmInteractor, Depends(Stub(UserSignInConfirmInteractor))
	],
):
	return await interactor(request_data)
