from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.interactors.token import RefreshTokenInteractor
from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import RefreshTokenRequestSchema
from sportify_auth.application.schemas.responses import RefreshTokenResponseSchema

refresh_router = APIRouter()


@refresh_router.post("/refresh", response_model=RefreshTokenResponseSchema)
async def refresh_token(
	request_data: RefreshTokenRequestSchema,
	interactor: Annotated[RefreshTokenInteractor, Depends(Stub(RefreshTokenInteractor))],
):
	return await interactor(request_data)
