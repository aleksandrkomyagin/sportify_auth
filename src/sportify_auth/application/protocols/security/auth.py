from typing import Protocol


class IAuthenticateService(Protocol):
    def __call__(self, authorization_header: str | None) -> None:
        pass
