from uuid import UUID

from fastapi import APIRouter, Depends, Header

from src.annotations.application.dtos.create_highlight_dto import CreateHighlightInputDto
from src.annotations.application.dtos.update_note_dto import UpdateNoteInputDto
from src.annotations.application.use_cases.create_highlight import CreateHighlightUseCase
from src.annotations.application.use_cases.list_highlights import ListHighlightsUseCase
from src.annotations.application.use_cases.delete_highlight import DeleteHighlightUseCase
from src.annotations.application.use_cases.update_note import UpdateNoteUseCase
from src.annotations.core.dependencies import (
    get_annotations_uow,
    get_create_highlight_use_case,
    get_list_highlights_use_case,
    get_delete_highlight_use_case,
    get_update_note_use_case,
    get_current_user_id,
)
from src.annotations.domain.exceptions import HighlightNotFoundError
from src.annotations.presentation.http.api.v1.endpoints.highlights.models import (
    CreateHighlightRequest,
    UpdateHighlightRequest,
    HighlightResponse,
    LocatorModel,
    ListHighlightsResponse,
)
from src.annotations.presentation.http.response import make_response

router = APIRouter(prefix="/highlights", tags=["highlights"])


def _to_locator(locator) -> LocatorModel:
    return LocatorModel(
        book_id=locator.book_id,
        chapter_number=locator.chapter.number if locator.chapter else None,
        chapter_title=locator.chapter.title if locator.chapter else None,
        value=locator.value,
        provider=locator.provider,
        sort_key=locator.sort_key,
    )


def _to_response(highlight) -> HighlightResponse:
    return HighlightResponse(
        id=highlight.id,
        selected_text=highlight.selected_text,
        color=highlight.color,
        note=highlight.note.value if highlight.note else None,
        locator=_to_locator(highlight.locator),
        end_locator=_to_locator(highlight.end_locator),
        is_deleted=highlight.is_deleted,
        created_at=highlight.created_at,
        updated_at=highlight.updated_at,
    )


@router.post("")
async def create_highlight(
    body: CreateHighlightRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: CreateHighlightUseCase = Depends(get_create_highlight_use_case),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    # The Idempotency-Key header is accepted for client-side idempotency.
    # (Dedup / replay protection can be layered on top of the created resource.)
    highlight = await use_case.execute(
        CreateHighlightInputDto(
            user_id=user_id,
            book_id=body.book_id,
            selected_text=body.selected_text,
            color=body.color,
            start_value=body.start_value,
            start_provider=body.start_provider,
            start_sort_key=body.start_sort_key,
            start_chapter_number=body.start_chapter_number,
            start_chapter_title=body.start_chapter_title,
            end_value=body.end_value,
            end_provider=body.end_provider,
            end_sort_key=body.end_sort_key,
            end_chapter_number=body.end_chapter_number,
            end_chapter_title=body.end_chapter_title,
            note=body.note,
        )
    )
    return make_response(data=_to_response(highlight), code=201)


@router.get("/books/{book_id}/highlights")
async def list_highlights(
    book_id: UUID,
    chapter: int | None = None,
    user_id: UUID = Depends(get_current_user_id),
    use_case: ListHighlightsUseCase = Depends(get_list_highlights_use_case),
):
    result = await use_case.execute(user_id, book_id, chapter)
    items = [_to_response(h) for h in result]
    return make_response(data=ListHighlightsResponse(items=items, total=len(items)))


@router.get("/{highlight_id}")
async def get_highlight(
    highlight_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    uow=Depends(get_annotations_uow),
):
    async with uow:
        highlight = await uow.highlights.query.find_by_id(highlight_id)
    if highlight is None:
        raise HighlightNotFoundError(f"Highlight {highlight_id} not found")
    return make_response(data=_to_response(highlight))


@router.patch("/{highlight_id}")
async def update_highlight(
    highlight_id: UUID,
    body: UpdateHighlightRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: UpdateNoteUseCase = Depends(get_update_note_use_case),
    uow=Depends(get_annotations_uow),
):
    async with uow:
        existing = await uow.highlights.query.find_by_id(highlight_id)
    if existing is None:
        raise HighlightNotFoundError(f"Highlight {highlight_id} not found")

    result = await use_case.execute(UpdateNoteInputDto(highlight_id=highlight_id, note=body.note))
    if body.color is not None:
        result.change_color(body.color)
        async with uow:
            await uow.highlights.command.save(result)
    return make_response(data=_to_response(result))


@router.delete("/{highlight_id}")
async def delete_highlight(
    highlight_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: DeleteHighlightUseCase = Depends(get_delete_highlight_use_case),
):
    # Idempotent: repeat DELETE returns 204 regardless.
    await use_case.execute(highlight_id)
    return make_response(message="Highlight deleted", code=204)