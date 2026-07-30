from dataclasses import dataclass
from uuid import UUID

from src.library.application.dtos.shelf_output_dto import ShelfBookOutputDto
from src.library.domain.exceptions import ShelfNotFoundError
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class GetShelfBooksUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, shelf_id: UUID) -> list[ShelfBookOutputDto]:
        async with self.uow as uow:
            shelf = await uow.shelves.query.find_by_id(shelf_id)
            if shelf is None:
                raise ShelfNotFoundError(f"Shelf {shelf_id} not found")

            book_ids = shelf.book_ids
            books = await uow.books.query.find_by_ids(book_ids)

            book_map = {book.id: book for book in books}

            result = []
            for assoc in shelf.book_associations:
                book = book_map.get(assoc.book_id)
                if book is not None:
                    result.append(
                        ShelfBookOutputDto(
                            id=book.id,
                            title=book.metadata.title,
                            author_first_name=book.metadata.author.first_name,
                            author_last_name=book.metadata.author.last_name,
                            isbn=str(book.metadata.isbn),
                            position=assoc.position,
                            is_starred=book.is_starred,
                        )
                    )

            return result