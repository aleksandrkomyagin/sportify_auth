from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserSignUpRequestSchema
from sportify_auth.application.schemas.responses import UserSignUpResponseSchema
from sportify_auth.application.interactors.user import UserSignUpInteractor


signup_router = APIRouter()


@signup_router.post("/signup", response_model=UserSignUpResponseSchema)
async def signup(
	request_data: UserSignUpRequestSchema,
	interactor: Annotated[UserSignUpInteractor, Depends(Stub(UserSignUpInteractor))],
):
	return await interactor(request_data)

