from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.library.infrastructure.sql.models.base import Base

if TYPE_CHECKING:
    from src.library.infrastructure.sql.models.book_model import BookModel
    from src.library.infrastructure.sql.models.shelf_model import ShelfModel


class ShelfBookAssociation(Base):
    __tablename__ = "shelf_books"

    shelf_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("shelves.id", ondelete="CASCADE"),
        primary_key=True,
    )
    book_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    shelf: Mapped[ShelfModel] = relationship(
        "ShelfModel", back_populates="book_associations"
    )
    book: Mapped[BookModel] = relationship(
        "BookModel", back_populates="shelf_associations"
    )