from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import RevokeTokenRequestSchema
from sportify_auth.application.schemas.responses import RevokeTokenResponseSchema
from sportify_auth.application.interactors.token import RevokeTokenInteractor
from sportify_auth.presentation.auth import authenticate

revoke_router = APIRouter(dependencies=[Depends(authenticate)])


@revoke_router.post("/revoke", response_model=RevokeTokenResponseSchema)
async def revoke_token(
	request_data: RevokeTokenRequestSchema,
	interactor: Annotated[RevokeTokenInteractor, Depends(Stub(RevokeTokenInteractor))],
):
	return await interactor(request_data)
