from dataclasses import dataclass

from ..validator import ValidatedDataClass


@dataclass
class BaseMessageResponse(ValidatedDataClass):
	message: str


@dataclass
class RefreshTokenResponseSchema(ValidatedDataClass):
	access_token: str
	refresh_token: str


class GenerateNewJWKSResponseSchema(BaseMessageResponse):
	pass


class RevokeTokenResponseSchema(BaseMessageResponse):
	pass
