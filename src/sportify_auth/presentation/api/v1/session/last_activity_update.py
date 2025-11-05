from typing import Annotated

from fastapi import APIRouter, Depends

from sportify_auth.application.interactors.session import SessionLastActivityUpdateInteractor
from sportify_auth.application.providers.stub import Stub
from sportify_auth.application.schemas.requests import SessionLastActivityUpdateRequestSchema

last_activity_update_router = APIRouter()


@last_activity_update_router.post("/last_activity_update", response_model=None)
async def last_activity_update(
	request_data: SessionLastActivityUpdateRequestSchema,
	interactor: Annotated[SessionLastActivityUpdateInteractor, Depends(Stub(SessionLastActivityUpdateInteractor))],
):
	return await interactor(request_data)
