from dataclasses import dataclass


@dataclass
class TokenDTO:
	access_token: str
	refresh_token: str
