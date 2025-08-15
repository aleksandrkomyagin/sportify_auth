from sportify_auth.infrastructure.common.exceptions.base import BaseInfraException


class StorageException(BaseInfraException):
    status_code: int = 500
