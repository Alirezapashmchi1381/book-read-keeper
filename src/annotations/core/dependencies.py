from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.dependencies.database import get_session_factory
from src.shared.auth.dependencies import get_current_user_id  # noqa: F401 – re-exported
from src.annotations.application.use_cases.create_highlight import CreateHighlightUseCase
from src.annotations.application.use_cases.list_highlights import ListHighlightsUseCase
from src.annotations.application.use_cases.delete_highlight import DeleteHighlightUseCase
from src.annotations.application.use_cases.update_note import UpdateNoteUseCase
from src.annotations.infrastructure.sql.unit_of_work.annotations import SQLAlchemyAnnotationsUnitOfWork


def get_annotations_uow(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> SQLAlchemyAnnotationsUnitOfWork:
    return SQLAlchemyAnnotationsUnitOfWork(session_factory)


AnnotationsUoWDep = Annotated[SQLAlchemyAnnotationsUnitOfWork, Depends(get_annotations_uow)]


def get_create_highlight_use_case(
    uow: AnnotationsUoWDep,
) -> CreateHighlightUseCase:
    return CreateHighlightUseCase(uow=uow)


def get_list_highlights_use_case(
    uow: AnnotationsUoWDep,
) -> ListHighlightsUseCase:
    return ListHighlightsUseCase(uow=uow)


def get_delete_highlight_use_case(
    uow: AnnotationsUoWDep,
) -> DeleteHighlightUseCase:
    return DeleteHighlightUseCase(uow=uow)


def get_update_note_use_case(
    uow: AnnotationsUoWDep,
) -> UpdateNoteUseCase:
    return UpdateNoteUseCase(uow=uow)