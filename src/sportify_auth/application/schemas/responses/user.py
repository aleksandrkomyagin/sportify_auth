from dataclasses import dataclass

from ..validator import ValidatedDataClass


@dataclass
class BaseMessageResponse(ValidatedDataClass):
    message: str


@dataclass
class BaseTokenDataResponse(ValidatedDataClass):
    access_token: str
    refresh_token: str


@dataclass
class UserSignUpResponseSchema(BaseMessageResponse):
    pass


@dataclass
class UserSignUpConfirmResponseSchema(BaseTokenDataResponse):
    pass


@dataclass
class UserSignInResponseSchema(BaseMessageResponse):
    pass


@dataclass
class UserSignInConfirmResponseSchema(BaseTokenDataResponse):
    pass


@dataclass
class UserActivateResponseSchema(BaseMessageResponse):
    pass


@dataclass
class UserActivateConfirmResponseSchema(BaseMessageResponse):
    pass


@dataclass
class UserDeactivateResponseSchema(BaseMessageResponse):
    pass
