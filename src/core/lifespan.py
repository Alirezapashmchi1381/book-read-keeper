from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import get_settings
from src.core.dependencies.database import get_engine
from src.annotations.infrastructure.sql.models.base import Base as AnnotationsBase
from src.identity.infrastructure.sql.models.base import Base
from src.storage.infrastructure.sql.models.base import Base as StorageBase

# Import all models so SQLAlchemy registers them with Base.metadata before create_all
import src.identity.infrastructure.sql.models.user_model  # noqa: F401
import src.identity.infrastructure.sql.models.refresh_token_model  # noqa: F401
import src.identity.infrastructure.sql.models.email_verification_token_model  # noqa: F401
import src.identity.infrastructure.sql.models.password_reset_token_model  # noqa: F401
import src.annotations.infrastructure.sql.models.highlight_model  # noqa: F401
import src.storage.infrastructure.sql.models.object_model  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = get_engine(settings.database_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(StorageBase.metadata.create_all)
        await conn.run_sync(AnnotationsBase.metadata.create_all)

    yield

    await engine.dispose()
