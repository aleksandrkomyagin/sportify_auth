from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserActivateRequestSchema
from sportify_auth.application.schemas.responses import UserActivateResponseSchema
from sportify_auth.application.interactors.user import UserActivateInteractor

activate_router = APIRouter()


@activate_router.post("/activate", response_model=UserActivateResponseSchema)
async def activate(
	request_data: UserActivateRequestSchema,
	interactor: Annotated[UserActivateInteractor, Depends(Stub(UserActivateInteractor))],
):
	return await interactor(request_data)
