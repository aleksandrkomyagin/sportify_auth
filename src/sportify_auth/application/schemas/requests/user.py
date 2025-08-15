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
class UserSignUpRequestSchema(BaseModelWithPhone):
    pass


@dataclass
class UserSignUpConfirmRequestSchema(BaseModelWithCode, BaseModelWithPhone):
    pass


@dataclass
class UserSignInRequestSchema(BaseModelWithPhone):
    pass


@dataclass
class UserSignInConfirmRequestSchema(BaseModelWithCode, BaseModelWithPhone):
    pass


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
