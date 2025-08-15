from typing import Annotated

from fastapi import Depends, Request

from sportify_auth.application.protocols.security.auth import IAuthenticateService
from sportify_auth.application.providers.stub import Stub


def authenticate(
    request: Request,
    authentication_service: Annotated[IAuthenticateService, Depends(Stub(IAuthenticateService))]
):
    authorization_header = request.headers.get("Authorization")
    return authentication_service(authorization_header)
