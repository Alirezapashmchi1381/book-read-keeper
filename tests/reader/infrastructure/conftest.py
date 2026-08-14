import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.reader.infrastructure.sql.models.base import Base
from src.reader.infrastructure.sql.models.reading_session_model import ReadingSessionModel  # noqa: F401
from src.reader.infrastructure.sql.unit_of_work.reader import SQLAlchemyReaderUnitOfWork


@pytest.fixture
async def session_factory():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False)
    yield factory

    await engine.dispose()


@pytest.fixture
async def session(session_factory):
    async with session_factory() as session:
        yield session


@pytest.fixture
async def reader_uow(session_factory) -> SQLAlchemyReaderUnitOfWork:
    return SQLAlchemyReaderUnitOfWork(session_factory)