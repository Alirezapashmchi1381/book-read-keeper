from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env.dev"),  # overridable
        env_file_encoding="utf-8",
        extra="ignore"
    )

    database_url: str = "sqlite+aiosqlite:///./dev.db"
    jwt_secret: str   # must be set
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    token_secret: str #  must be set
    cors_origins: list[str] = ["*"]
    debug: bool = False

@lru_cache
def get_settings() -> Settings:
    return Settings()
