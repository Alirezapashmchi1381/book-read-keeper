from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateShelfRequest(BaseModel):
    name: str
    color: str = "#ffffff"


class UpdateShelfRequest(BaseModel):
    name: str | None = None
    color: str | None = None


class AddBookToShelfRequest(BaseModel):
    book_id: UUID


class ReorderShelfRequest(BaseModel):
    book_ids: list[UUID]


class ShelfResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    color: str
    book_count: int
    is_starred: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class ShelfBookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    author_first_name: str
    author_last_name: str
    isbn: str
    position: int
    is_starred: bool