from logging import getLogger

from sportify_auth.adapters.mappers.user_mapper import UserMapper
from sportify_auth.application.protocols.repositories.user.user_repository import IUserRepository

from .consumer import get_consumer

logger = getLogger(__name__)

consumer = get_consumer()


@consumer.subscriber("update_user")
async def update_handler(message: dict, repo: IUserRepository) -> None:
	user_id = message.pop("id")
	await repo.update_user(user_id, UserMapper.to_update(message))
