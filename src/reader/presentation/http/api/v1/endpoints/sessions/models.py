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


class StartSessionRequest(BaseModel):
    book_id: UUID
    locator_value: str
    locator_provider: str
    locator_sort_key: str
    locator_chapter_number: int | None = None
    locator_chapter_title: str | None = None
    device_id: str | None = None


class UpsertProgressRequest(BaseModel):
    locator_value: str
    locator_provider: str
    locator_sort_key: str
    locator_chapter_number: int | None = None
    locator_chapter_title: str | None = None
    progress_percent: float | None = None
    device_id: str | None = None


class SessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    locator: LocatorModel
    progress_percent: float
    device_id: str | None
    started_at: datetime
    updated_at: datetime