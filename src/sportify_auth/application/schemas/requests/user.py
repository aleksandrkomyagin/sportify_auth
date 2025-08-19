from dataclasses import dataclass

from ..validator import ValidatedDataClass


@dataclass
class BaseModelWithCode(ValidatedDataClass):
	code: str


@dataclass
class BaseModelWithPhone(ValidatedDataClass):
	phone: str


@dataclass
class BaseModelWithUserID(ValidatedDataClass):
	user_id: str


@dataclass
class ConfirmData(BaseModelWithCode, BaseModelWithPhone):
	pass


@dataclass
class DeviceInfo:
	device_id: str
	device_type: str
	device_name: str
	os_version: str
	push_token: str


@dataclass
class UserSignUpRequestSchema(BaseModelWithPhone):
	pass


@dataclass
class UserSignUpConfirmRequestSchema:
	signup_confirm_data: ConfirmData
	device_info: DeviceInfo


@dataclass
class UserSignInRequestSchema(BaseModelWithPhone):
	pass


@dataclass
class UserSignInConfirmRequestSchema:
	signin_confirm_data: ConfirmData
	device_info: DeviceInfo


@dataclass
class UserSignOutRequestSchema(BaseModelWithUserID):
	session_ids: list[str]
	delete_devices: bool


@dataclass
class UserDeleteRequestSchema(BaseModelWithUserID):
	pass


@dataclass
class UserActivateRequestSchema(BaseModelWithPhone):
	pass


@dataclass
class UserActivateConfirmRequestSchema(BaseModelWithCode, BaseModelWithPhone):
	pass


@dataclass
class UserDeactivateRequestSchema(BaseModelWithUserID):
	pass
