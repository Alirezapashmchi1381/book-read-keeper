from uuid import UUID

from fastapi import APIRouter, Depends

from src.reader.application.dtos.start_session_dto import StartSessionInputDto
from src.reader.application.dtos.upsert_progress_dto import UpsertProgressInputDto
from src.reader.application.use_cases.start_session import StartSessionUseCase
from src.reader.application.use_cases.upsert_progress import UpsertProgressUseCase
from src.reader.application.use_cases.get_progress import GetProgressUseCase
from src.reader.core.dependencies import (
    get_reader_uow,
    get_start_session_use_case,
    get_upsert_progress_use_case,
    get_get_progress_use_case,
    get_current_user_id,
)
from src.reader.domain.exceptions import ReadingSessionNotFoundError
from src.reader.presentation.http.api.v1.endpoints.sessions.models import (
    StartSessionRequest,
    UpsertProgressRequest,
    SessionResponse,
    LocatorModel,
)
from src.reader.presentation.http.response import make_response

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _to_locator(locator) -> LocatorModel:
    return LocatorModel(
        book_id=locator.book_id,
        chapter_number=locator.chapter_number,
        chapter_title=locator.chapter_title,
        value=locator.value,
        provider=locator.provider,
        sort_key=locator.sort_key,
    )


def _to_response(session) -> SessionResponse:
    return SessionResponse(
        id=session.id,
        user_id=session.user_id,
        book_id=session.book_id,
        locator=_to_locator(session.locator),
        progress_percent=session.progress_percent.value,
        device_id=session.device_id.value if session.device_id else None,
        started_at=session.started_at,
        updated_at=session.updated_at,
    )


@router.post("")
async def start_session(
    body: StartSessionRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: StartSessionUseCase = Depends(get_start_session_use_case),
):
    session = await use_case.execute(
        StartSessionInputDto(
            user_id=user_id,
            book_id=body.book_id,
            locator_value=body.locator_value,
            locator_provider=body.locator_provider,
            locator_sort_key=body.locator_sort_key,
            locator_chapter_number=body.locator_chapter_number,
            locator_chapter_title=body.locator_chapter_title,
            device_id=body.device_id,
        )
    )
    return make_response(data=_to_response(session), code=201)


@router.patch("/books/{book_id}")
async def upsert_progress(
    book_id: UUID,
    body: UpsertProgressRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: UpsertProgressUseCase = Depends(get_upsert_progress_use_case),
):
    session = await use_case.execute(
        UpsertProgressInputDto(
            user_id=user_id,
            book_id=book_id,
            locator_value=body.locator_value,
            locator_provider=body.locator_provider,
            locator_sort_key=body.locator_sort_key,
            locator_chapter_number=body.locator_chapter_number,
            locator_chapter_title=body.locator_chapter_title,
            progress_percent=body.progress_percent,
            device_id=body.device_id,
        )
    )
    return make_response(data=_to_response(session))


@router.get("/books/{book_id}")
async def get_progress(
    book_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: GetProgressUseCase = Depends(get_get_progress_use_case),
):
    session = await use_case.execute(user_id, book_id)
    return make_response(data=_to_response(session))