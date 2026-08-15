from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.dependencies.database import get_session_factory
from src.shared.auth.dependencies import get_current_user_id  # noqa: F401 – re-exported
from src.reader.application.use_cases.start_session import StartSessionUseCase
from src.reader.application.use_cases.upsert_progress import UpsertProgressUseCase
from src.reader.application.use_cases.get_progress import GetProgressUseCase
from src.reader.infrastructure.sql.unit_of_work.reader import SQLAlchemyReaderUnitOfWork


def get_reader_uow(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> SQLAlchemyReaderUnitOfWork:
    return SQLAlchemyReaderUnitOfWork(session_factory)


ReaderUoWDep = Annotated[SQLAlchemyReaderUnitOfWork, Depends(get_reader_uow)]


def get_start_session_use_case(
    uow: ReaderUoWDep,
) -> StartSessionUseCase:
    return StartSessionUseCase(uow=uow)


def get_upsert_progress_use_case(
    uow: ReaderUoWDep,
) -> UpsertProgressUseCase:
    return UpsertProgressUseCase(uow=uow)


def get_get_progress_use_case(
    uow: ReaderUoWDep,
) -> GetProgressUseCase:
    return GetProgressUseCase(uow=uow)