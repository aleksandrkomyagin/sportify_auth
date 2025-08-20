import uuid

from datetime import datetime, timedelta
from logging import getLogger
from typing import Any

import jwt

from sportify_auth.application.dto.event import NewOutboxEventDTO
from sportify_auth.application.dto.token import RefreshTokenRequest, TokenDTO, TokenData
from sportify_auth.application.dto.user import UserIdDTO
from sportify_auth.application.exceptions.token import (
	InvalidTokenException,
	InvalidTokenIssuerException,
	InvalidTokenJTIException,
	InvalidTokenTypeException,
	JWKNotFoundException,
	JWKSNotFoundException,
	MakeTokenException,
	RSAKeyNotFoundException,
	TokenExpiredException,
	TokenIsRevokedException,
)
from sportify_auth.application.protocols.cache import ICacheService
from sportify_auth.application.protocols.file_storages.base import IJWKStorage
from sportify_auth.application.protocols.key_generator.base import IKeyGenerator
from sportify_auth.application.protocols.services import ITokenService
from sportify_auth.application.schemas.requests import RevokeTokenRequestSchema
from sportify_auth.setup.config import settings

logger = getLogger(__name__)


class TokenService(ITokenService):
	def __init__(
		self,
		cache_service: ICacheService,
		file_storage: IJWKStorage,
		rsa_key_generator: IKeyGenerator,
	) -> None:
		self._cache = cache_service
		self._file_storage = file_storage
		self._rsa_key_generator = rsa_key_generator

	async def _get_current_rsa_key(self) -> list[str]:
		return await self._cache.get(settings.redis.jwks_db, "current_rsa_key")

	async def _get_jwk(self, kid: str) -> dict[str, Any]:
		jwks = await self._cache.get(settings.redis.jwks_db, "JWKS")
		if jwks is None:
			raise JWKSNotFoundException(message="JWKS не найдены")
		key = None
		for k in jwks:
			if k["kid"] == kid:
				key = k
				break
		if key is None:
			raise JWKNotFoundException(message="Ключ не найден")
		return key

	@staticmethod
	def _make_payload(user_id: str, expire: datetime, token_type: str) -> dict:
		return {
			"user_id": user_id,
			"exp": expire,
			"jti": str(uuid.uuid4()),
			"iss": settings.token_config.issuer,
			"type": token_type,
		}

	async def _validate_token_payload(self, payload: dict[str, Any]) -> str:
		jti = payload.get("jti", None)
		if not jti:
			raise InvalidTokenJTIException(message="Некорректный токен")

		token = await self._cache.get(settings.redis.revoked_token_db, f"revoked:{jti}")
		if token:
			raise TokenIsRevokedException(message="Токен отозван")

		token_type = payload.get("type", None)
		if not token_type or token_type != "refresh":
			raise InvalidTokenTypeException(message="Неверный тип токена")

		issuer = payload.get("iss", None)
		if not issuer or issuer != settings.token_config.issuer:
			raise InvalidTokenIssuerException(message="Неверный издатель токена")

		return payload["user_id"]

	async def _get_public_key_from_jwks(self, kid: str) -> str:
		jwk = await self._get_jwk(kid)
		return await self._rsa_key_generator.generate_public_key_from_jwk(jwk)

	async def _decode_token(self, token: str) -> dict[str, Any]:
		try:
			unverified_header = jwt.get_unverified_header(token)
			kid = unverified_header["kid"]
			public_key = await self._get_public_key_from_jwks(kid)

			payload = jwt.decode(
				jwt=token,
				key=public_key,
				algorithms=settings.token_config.algorithm,
				issuer=settings.token_config.issuer,
			)
		except jwt.ExpiredSignatureError as e:
			raise TokenExpiredException(message="Срок действия токена истек") from e
		except jwt.InvalidTokenError as e:
			raise InvalidTokenException(message="Некорректный токен") from e
		except jwt.PyJWTError as e:
			raise InvalidTokenException(message="Некорректный токен") from e

		return payload

	async def _make_token(self, user_id: str) -> dict[str, TokenData]:
		current_rsa_key = await self._get_current_rsa_key()
		if not current_rsa_key:
			raise RSAKeyNotFoundException(message="Ключ RSA не создан")
		kid, private_pem = current_rsa_key
		try:
			access_token_expire = datetime.now() + timedelta(minutes=10)
			refresh_token_expire = datetime.now() + timedelta(days=1)
			access_token = jwt.encode(
				payload=self._make_payload(user_id, access_token_expire, "access"),
				key=private_pem,
				algorithm=settings.token_config.algorithm,
				headers={"kid": kid},
			)
			refresh_token = jwt.encode(
				payload=self._make_payload(user_id, refresh_token_expire, "refresh"),
				key=private_pem,
				algorithm=settings.token_config.algorithm,
				headers={"kid": kid},
			)
		except jwt.PyJWTError as e:
			raise MakeTokenException(message="Ошибка создания токена") from e
		return {
			"access_token": TokenData(token=access_token, expires_at=access_token_expire),
			"refresh_token": TokenData(token=refresh_token, expires_at=refresh_token_expire),
		}

	async def generate_new_rsa_key(self) -> str:
		"""
		Генерация нового ключа RSA. Возвращает старый ключ, для дальнейшей его передачи
		в отложенную задачу
		"""
		current_key = await self._get_current_rsa_key()
		old_kid = current_key[0] if current_key else None
		kid = str(uuid.uuid4())
		rsa_key_data = await self._rsa_key_generator.generate_rsa()

		new_jwk = {
			"kid": kid,
			"use": "sig",
			"alg": settings.token_config.algorithm,
			"n": rsa_key_data.n,
			"e": rsa_key_data.e,
			"public_key_pem": rsa_key_data.public_pem,
		}
		await self._file_storage.add([new_jwk])
		await self._cache.append(
			settings.redis.jwks_db,
			"JWKS",
			new_jwk,
		)
		await self._cache.set(
			settings.redis.jwks_db, "current_rsa_key", [kid, rsa_key_data.private_pem]
		)

		return old_kid

	async def get_jwks(self) -> list[dict[str, Any]]:
		keys = await self._cache.get(settings.redis.jwks_db, "JWKS")
		if not keys:
			raise JWKSNotFoundException(message="JWKS не найдены")
		return keys

	async def create_token(self, user_id: UserIdDTO) -> TokenDTO:
		token = await self._make_token(str(user_id.id))
		return TokenDTO(access_token=token["access_token"], refresh_token=token["refresh_token"])

	async def revoke_token(self, token_data: RevokeTokenRequestSchema) -> NewOutboxEventDTO:
		payload = await self._decode_token(token_data.refresh_token)
		exp_dt = datetime.fromtimestamp(payload["exp"])
		await self._cache.set(
			settings.redis.revoked_token_db,
			f"revoked:{payload['jti']}",
			"1",
			expire=int((exp_dt - datetime.now()).total_seconds()),
		)
		return NewOutboxEventDTO(
			topic="revoke_token",
			payload={"jti": payload["jti"]},
		)

	async def refresh_token(self, token_data: RefreshTokenRequest) -> TokenDTO:
		payload = await self._decode_token(token_data.refresh_token)
		user_id = await self._validate_token_payload(payload)
		token = await self._make_token(user_id)
		exp_dt = datetime.fromtimestamp(payload["exp"])
		await self._cache.set(
			settings.redis.revoked_token_db,
			f"revoked:{payload['jti']}",
			"1",
			expire=int((exp_dt - datetime.now()).total_seconds()),
		)
		return TokenDTO(access_token=token["access_token"], refresh_token=token["refresh_token"])
