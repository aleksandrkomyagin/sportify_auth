from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sportify_auth.application.protocols.security.auth import IAuthenticateService
from sportify_auth.application.providers.stub import Stub

security = HTTPBearer(auto_error=False)


def authenticate(
	authentication_service: Annotated[IAuthenticateService, Depends(Stub(IAuthenticateService))],
	credentials: HTTPAuthorizationCredentials = Security(security),
):
	authorization_data = f"{credentials.scheme} {credentials.credentials}" if credentials else None
	return authentication_service(authorization_data)
