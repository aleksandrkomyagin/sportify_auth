from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenData:
	token: str
	expires_at: datetime


@dataclass
class TokenDTO:
	access_token: TokenData
	refresh_token: TokenData


@dataclass
class RefreshTokenRequest:
	refresh_token: str
