from dataclasses import dataclass

from src.library.application.dtos.update_book_metadata_dto import UpdateBookMetadataInputDto
from src.library.domain.entities.book import Book
from src.library.domain.exceptions import BookNotFoundError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork
from src.library.domain.value_objects.author import Author
from src.library.domain.value_objects.book_metadata import BookMetadata
from src.library.domain.value_objects.color import Color
from src.library.domain.value_objects.isbn import ISBN
from src.library.domain.value_objects.language import Language


@dataclass
class UpdateBookMetadataUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, dto: UpdateBookMetadataInputDto) -> Book:
        async with self.uow as uow:
            book = await uow.books.query.find_by_id(dto.book_id)
            if book is None:
                raise BookNotFoundError(f"Book {dto.book_id} not found")

            # Update metadata fields
            metadata = book.metadata
            new_metadata = BookMetadata(
                author=Author(
                    first_name=dto.author_first_name if dto.author_first_name is not None else metadata.author.first_name,
                    last_name=dto.author_last_name if dto.author_last_name is not None else metadata.author.last_name,
                ),
                isbn=ISBN(dto.isbn) if dto.isbn is not None else metadata.isbn,
                title=dto.title if dto.title is not None else metadata.title,
                language=Language(dto.language) if dto.language is not None else metadata.language,
                color=Color(dto.color) if dto.color is not None else metadata.color,
                description=dto.description if dto.description is not None else metadata.description,
            )
            book.update_metadata(new_metadata)

            # Handle star/unstar
            if dto.is_starred is True:
                book.mark_as_starred()
            elif dto.is_starred is False:
                book.unstar()

            await uow.books.command.save(book)
            await uow.commit()
            return book