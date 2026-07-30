from dataclasses import dataclass

from src.library.application.dtos.upload_book_cover_dto import UploadBookCoverInputDto
from src.library.domain.entities.book import Book
from src.library.domain.exceptions import BookNotFoundError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork
from src.library.domain.ports.file_storage_service import FileStorageService
from src.library.domain.value_objects.mime_type import MimeType


@dataclass
class UploadBookCoverUseCase:
    uow: LibraryUnitOfWork
    file_storage: FileStorageService

    async def execute(self, dto: UploadBookCoverInputDto) -> Book:
        async with self.uow as uow:
            book = await uow.books.query.find_by_id(dto.book_id)
            if book is None:
                raise BookNotFoundError(f"Book {dto.book_id} not found")

            mime_type = MimeType(dto.mime_type)
            cover = await self.file_storage.store_cover(
                book_id=dto.book_id,
                content=dto.content,
                mime_type=mime_type,
            )
            book.attach_cover(cover)
            await uow.books.command.save(book)
            await uow.commit()
            return book