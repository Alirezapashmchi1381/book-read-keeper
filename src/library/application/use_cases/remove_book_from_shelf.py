from dataclasses import dataclass

from src.library.application.dtos.remove_book_from_shelf_dto import RemoveBookFromShelfInputDto
from src.library.domain.entities.shelf import Shelf
from src.library.domain.exceptions import (
    BookNotFoundError,
    ShelfNotFoundError,
    BookNotInShelfError,
)
from src.library.domain.ports.unit_of_work import LibraryUnitOfWork


@dataclass
class RemoveBookFromShelfUseCase:
    uow: LibraryUnitOfWork

    async def execute(self, dto: RemoveBookFromShelfInputDto) -> Shelf:
        async with self.uow as uow:
            book = await uow.books.query.find_by_id(dto.book_id)
            if book is None:
                raise BookNotFoundError(f"Book {dto.book_id} not found")

            shelf = await uow.shelves.query.find_by_id(dto.shelf_id)
            if shelf is None:
                raise ShelfNotFoundError(f"Shelf {dto.shelf_id} not found")

            if not shelf.has_book(dto.book_id):
                raise BookNotInShelfError(
                    f"Book {dto.book_id} is not in shelf {dto.shelf_id}"
                )

            shelf.remove_book(dto.book_id)
            await uow.shelves.command.save(shelf)
            await uow.commit()
            return shelf