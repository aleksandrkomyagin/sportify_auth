from dataclasses import dataclass


@dataclass
class UserIdDTO:
	id: str


@dataclass
class UserDTO:
	id: str
	phone: str
	created_at: str
	is_active: bool


@dataclass
class UserConfirmRequest:
	code: str
	phone: str


class UserSignInConfirmRequest(UserConfirmRequest):
	pass


class UserSignUpConfirmRequest(UserConfirmRequest):
	pass
