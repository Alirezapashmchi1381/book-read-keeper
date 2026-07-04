from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import get_settings
from src.core.dependencies.database import get_engine
from src.identity.infrastructure.sql.models.base import Base

# Import all models so SQLAlchemy registers them with Base.metadata before create_all
import src.identity.infrastructure.sql.models.user_model  # noqa: F401
import src.identity.infrastructure.sql.models.refresh_token_model  # noqa: F401
import src.identity.infrastructure.sql.models.email_verification_token_model  # noqa: F401
import src.identity.infrastructure.sql.models.password_reset_token_model  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = get_engine(settings.database_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()
