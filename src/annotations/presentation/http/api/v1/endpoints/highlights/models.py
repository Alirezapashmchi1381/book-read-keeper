from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LocatorModel(BaseModel):
    book_id: UUID
    chapter_number: int | None = None
    chapter_title: str | None = None
    value: str
    provider: str
    sort_key: str


class CreateHighlightRequest(BaseModel):
    book_id: UUID
    selected_text: str
    color: str
    start_value: str
    start_provider: str
    start_sort_key: str
    start_chapter_number: int | None = None
    start_chapter_title: str | None = None
    end_value: str
    end_provider: str
    end_sort_key: str
    end_chapter_number: int | None = None
    end_chapter_title: str | None = None
    note: str | None = None


class UpdateHighlightRequest(BaseModel):
    note: str | None = None
    color: str | None = None


class HighlightResponse(BaseModel):
    id: UUID
    selected_text: str
    color: str
    note: str | None
    locator: LocatorModel
    end_locator: LocatorModel
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class ListHighlightsResponse(BaseModel):
    items: list[HighlightResponse]
    total: int