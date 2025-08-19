import os

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class APIConfig(BaseSettings):
	host: str
	port: str
	log_level: str
	cors_origins: str
	debug: bool
	name_service: str
	workers: int = os.cpu_count()

	model_config = SettingsConfigDict(env_file=".env", env_prefix="API_", extra="ignore")


class SecurityConfig(BaseSettings):
	algorithm: str
	issuer: str
	secret_key: str

	model_config = SettingsConfigDict(env_file=".env", env_prefix="SECURITY_", extra="ignore")


class PostgresConfig(BaseSettings):
	db: str
	host: str
	user: str
	password: str
	port: str

	model_config = SettingsConfigDict(env_file=".env", env_prefix="POSTGRES_", extra="ignore")

	# @property
	def connection_string(self) -> str:
		url = "%s://%s:%s@%s:%s/%s" % (
			"postgresql+asyncpg",
			self.user,
			self.password,
			self.host,
			self.port,
			self.db,
		)

		return url


class RedisDatabase(BaseSettings):
	url: str
	user_db: str
	jwks_db: str
	code_db: str
	revoked_token_db: str
	tasks_db: str

	model_config = SettingsConfigDict(env_file=".env", env_prefix="REDIS_", extra="ignore")


class TokenConfig(BaseSettings):
	algorithm: str
	issuer: str
	expiration_time: int = 3600
	jwks_file_path: str = str(BASE_DIR / "static/.well-known/jwks.json")

	model_config = SettingsConfigDict(env_file=".env", env_prefix="TOKEN_", extra="ignore")


class Kafka(BaseSettings):
	server: str
	consumer_topics: str

	model_config = SettingsConfigDict(env_file=".env", env_prefix="KAFKA_", extra="ignore")


class Settings(BaseSettings):
	postgres: PostgresConfig = PostgresConfig()
	redis: RedisDatabase = RedisDatabase()
	api_config: APIConfig = APIConfig()
	token_config: TokenConfig = TokenConfig()
	kafka: Kafka = Kafka()
	security: SecurityConfig = SecurityConfig()


settings = Settings()
