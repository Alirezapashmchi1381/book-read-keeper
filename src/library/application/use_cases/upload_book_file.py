from dataclasses import dataclass

from src.library.application.dtos.upload_book_file_dto import UploadBookFileInputDto
from src.library.domain.entities.book import Book
from src.library.domain.exceptions import BookNotFoundError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork
from src.library.domain.ports.file_storage_service import FileStorageService
from src.library.domain.value_objects.file_format import FileFormat


@dataclass
class UploadBookFileUseCase:
    uow: LibraryUnitOfWork
    file_storage: FileStorageService

    async def execute(self, dto: UploadBookFileInputDto) -> Book:
        async with self.uow as uow:
            book = await uow.books.query.find_by_id(dto.book_id)
            if book is None:
                raise BookNotFoundError(f"Book {dto.book_id} not found")

            format = FileFormat(dto.format)
            book_file = await self.file_storage.store_book_file(
                book_id=dto.book_id,
                content=dto.content,
                format=format,
            )
            book.attach_book_file(book_file)
            await uow.books.command.save(book)
            await uow.commit()
            return book