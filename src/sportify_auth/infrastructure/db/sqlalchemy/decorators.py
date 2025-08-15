from functools import wraps
from logging import getLogger

from sqlalchemy.exc import SQLAlchemyError

from sportify_auth.infrastructure.exceptions.db.sql_alchemy import DatabaseOperationException

logger = getLogger(__name__)


def db_operation(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            logger.error("Ошибка запроса в базу данных: %s", str(e), exc_info=True)
            raise DatabaseOperationException(message="Ошибка запроса в базу данных") from e
    return wrapper
