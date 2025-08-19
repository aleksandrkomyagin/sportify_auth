import json
import os

from functools import lru_cache
from logging import getLogger
from typing import Any

import aiofiles

from sportify_auth.application.protocols.file_storages.base import IJWKStorage
from sportify_auth.infrastructure.exceptions.file_storage.jwk_storage import (
	StorageException,
)
from sportify_auth.setup.config import settings

logger = getLogger(__name__)


class JWKStorage(IJWKStorage):
	def __init__(self, file_path: str):
		self.file_path = file_path
		os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

	async def _load(self) -> list[dict[str, Any]]:
		if not os.path.exists(self.file_path):
			return []

		try:
			async with aiofiles.open(self.file_path, "r") as f:
				content = await f.read()
				return json.loads(content)
		except Exception as e:
			logger.error("Ошибка чтения JWKS: %s", str(e))
			raise StorageException(message="Ошибка чтения JWKS") from e

	async def _save(self, jwks: list[dict[str, Any]]) -> None:
		try:
			async with aiofiles.open(self.file_path, "w") as f:
				await f.write(json.dumps(jwks, indent=4))
		except Exception as e:
			logger.error("Ошибка сохранения JWKS: %s", str(e))
			raise StorageException(message="Ошибка сохранения JWKS") from e

	async def add(self, jwks: list[dict[str, Any]]) -> None:
		current_jwks = await self._load()
		current_jwks.extend(jwks)
		await self._save(current_jwks)

	async def replace(self, jwks: list[dict[str, Any]]) -> None:
		await self._save(jwks)


@lru_cache
def get_jwk_storage() -> JWKStorage:
	return JWKStorage(settings.token_config.jwks_file_path)
