from sportify_auth.infrastructure.common.exceptions.base import BaseServiceAuthException


class TokenRequiredException(BaseServiceAuthException):
    status_code = 401


class BearerSchemaRequiredException(BaseServiceAuthException):
    status_code = 401


class InvalidTokenException(BaseServiceAuthException):
    status_code = 403


class TokenExpiredException(BaseServiceAuthException):
    status_code = 401
