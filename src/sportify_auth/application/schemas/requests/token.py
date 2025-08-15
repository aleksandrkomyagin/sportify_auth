from dataclasses import dataclass

from ..validator import ValidatedDataClass


@dataclass
class BaseTokenRequestSchema(ValidatedDataClass):
	refresh_token: str


class RefreshTokenRequestSchema(BaseTokenRequestSchema):
	pass


class RevokeTokenRequestSchema(BaseTokenRequestSchema):
	pass
