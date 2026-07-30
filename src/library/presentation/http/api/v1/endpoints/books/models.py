from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateBookRequest(BaseModel):
    author_first_name: str
    author_last_name: str
    isbn: str
    title: str
    language: str = "en"
    color: str = "#ffffff"
    description: str | None = None


class UpdateBookMetadataRequest(BaseModel):
    author_first_name: str | None = None
    author_last_name: str | None = None
    isbn: str | None = None
    title: str | None = None
    language: str | None = None
    color: str | None = None
    description: str | None = None


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    author_first_name: str
    author_last_name: str
    isbn: str
    language: str
    color: str
    description: str | None
    is_starred: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class BookFileResponse(BaseModel):
    storage_key: str
    format: str
    checksum_algorithm: str
    checksum_value: str
    size_bytes: int
    mime_type: str


class BookCoverResponse(BaseModel):
    storage_key: str
    width: int
    height: int
    generated: bool


class SearchBooksResponse(BaseModel):
    items: list[BookResponse]
    total: int