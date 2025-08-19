from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.interactors.user import UserActivateConfirmInteractor
from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import UserActivateConfirmRequestSchema
from sportify_auth.application.schemas.responses import UserActivateConfirmResponseSchema

activate_confirm_router = APIRouter()


@activate_confirm_router.post("/activate_confirm", response_model=UserActivateConfirmResponseSchema)
async def activate(
	request_data: UserActivateConfirmRequestSchema,
	interactor: Annotated[
		UserActivateConfirmInteractor, Depends(Stub(UserActivateConfirmInteractor))
	],
):
	return await interactor(request_data)
