from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.library.infrastructure.sql.models.base import Base
from src.library.infrastructure.sql.models.shelf_model import ShelfModel

class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    shelf_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), ForeignKey("shelves.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author_first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    author_last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False)
    language: Mapped[str] = mapped_column(String(3), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    storage_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_format: Mapped[str | None] = mapped_column(String(20), nullable=True)
    checksum_algorithm: Mapped[str | None] = mapped_column(String(20), nullable=True)
    checksum_value: Mapped[str | None] = mapped_column(String(128), nullable=True)
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cover_storage_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cover_height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cover_generated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_starred: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    shelf: Mapped["ShelfModel"] = relationship("ShelfModel", back_populates="books")