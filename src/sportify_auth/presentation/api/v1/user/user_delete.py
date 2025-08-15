from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserDeleteRequestSchema
from sportify_auth.application.interactors.user import UserDeleteInteractor
from sportify_auth.presentation.auth import authenticate

delete_router = APIRouter(dependencies=[Depends(authenticate)])


@delete_router.post("/delete", status_code=204)
async def delete(
	request_data: UserDeleteRequestSchema,
	interactor: Annotated[UserDeleteInteractor, Depends(Stub(UserDeleteInteractor))],
):
	return await interactor(request_data)
