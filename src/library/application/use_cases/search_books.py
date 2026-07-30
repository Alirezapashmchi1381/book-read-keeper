from dataclasses import dataclass

from src.library.application.dtos.search_books_dto import SearchBooksInputDto, BookOutputDto
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class SearchBooksUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, dto: SearchBooksInputDto) -> list[BookOutputDto]:
        async with self.uow as uow:
            books = await uow.books.query.search_by_title(dto.title)

        return [
            BookOutputDto(
                id=book.id,
                title=book.metadata.title,
                author_first_name=book.metadata.author.first_name,
                author_last_name=book.metadata.author.last_name,
                isbn=str(book.metadata.isbn),
                language=book.metadata.language.code,
                color=book.metadata.color.hex_value,
                description=book.metadata.description,
                is_starred=book.is_starred,
                is_deleted=book.is_deleted,
                created_at=book.created_at,
                updated_at=book.updated_at,
            )
            for book in books
        ]