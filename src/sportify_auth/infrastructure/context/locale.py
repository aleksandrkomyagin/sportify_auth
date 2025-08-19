from contextvars import ContextVar

locale_var: ContextVar[str] = ContextVar("locale")
