from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserDeactivateRequestSchema
from sportify_auth.application.schemas.responses import UserDeactivateResponseSchema
from sportify_auth.application.interactors.user import UserDeactivateInteractor
from sportify_auth.presentation.auth import authenticate

deactivate_router = APIRouter(dependencies=[Depends(authenticate)])


@deactivate_router.post("/deactivate", response_model=UserDeactivateResponseSchema)
async def activate(
	request_data: UserDeactivateRequestSchema,
	interactor: Annotated[
		UserDeactivateInteractor, Depends(Stub(UserDeactivateInteractor))
	],
):
	return await interactor(request_data)
