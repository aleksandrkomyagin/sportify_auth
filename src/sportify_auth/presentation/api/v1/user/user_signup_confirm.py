from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserSignUpConfirmRequestSchema
from sportify_auth.application.schemas.responses import UserSignUpConfirmResponseSchema
from sportify_auth.application.interactors.user import UserSignUpConfirmInteractor

signup_confirm_router = APIRouter()


@signup_confirm_router.post(
	"/signup_confirm", response_model=UserSignUpConfirmResponseSchema
)
async def signup_confirm(
	request_data: UserSignUpConfirmRequestSchema,
	interactor: Annotated[
		UserSignUpConfirmInteractor, Depends(Stub(UserSignUpConfirmInteractor))
	],
):
	return await interactor(request_data)
