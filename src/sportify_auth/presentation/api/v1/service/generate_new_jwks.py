from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.responses import GenerateNewJWKSResponseSchema
from sportify_auth.application.interactors.token import GenerateNewJWKSInteractor

jwks_router = APIRouter()


@jwks_router.post("/generate_new_jwks", response_model=GenerateNewJWKSResponseSchema)
async def generate_new_jwks(
	interactor: Annotated[
		GenerateNewJWKSInteractor, Depends(Stub(GenerateNewJWKSInteractor))
	],
):
	return await interactor()
