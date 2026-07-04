from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import Settings, get_settings


@lru_cache
def _make_engine(database_url: str):
    return create_async_engine(database_url, pool_pre_ping=True)


def get_session_factory(
    settings: Settings = Depends(get_settings),
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(_make_engine(settings.database_url), expire_on_commit=False)
