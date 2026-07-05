from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dev", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = "sqlite+aiosqlite:///./dev.db"

    # JWT
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # Opaque token hashing (refresh / verification / reset tokens)
    token_secret: str = "change-token-secret-in-production"

    # CORS
    cors_origins: list[str] = ["*"]

    # App
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
