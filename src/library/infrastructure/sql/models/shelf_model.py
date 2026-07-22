from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.library.infrastructure.sql.models.base import Base
from src.library.infrastructure.sql.models.shelf_book_association import ShelfBookAssociation


class ShelfModel(Base):
    __tablename__ = "shelves"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    is_starred: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    book_associations: Mapped[list["ShelfBookAssociation"]] = relationship(
        "ShelfBookAssociation",
        back_populates="shelf",
        cascade="all, delete-orphan",
    )