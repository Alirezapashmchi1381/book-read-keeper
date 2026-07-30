from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.dependencies.database import get_session_factory
from src.library.application.use_cases.create_book import CreateBookUseCase
from src.library.application.use_cases.update_book_metadata import UpdateBookMetadataUseCase
from src.library.application.use_cases.upload_book_file import UploadBookFileUseCase
from src.library.application.use_cases.upload_book_cover import UploadBookCoverUseCase
from src.library.application.use_cases.star_book import StarBookUseCase
from src.library.application.use_cases.delete_book import DeleteBookUseCase
from src.library.application.use_cases.restore_book import RestoreBookUseCase
from src.library.application.use_cases.search_books import SearchBooksUseCase
from src.library.application.use_cases.create_shelf import CreateShelfUseCase
from src.library.application.use_cases.update_shelf import UpdateShelfUseCase
from src.library.application.use_cases.star_shelf import StarShelfUseCase
from src.library.application.use_cases.delete_shelf import DeleteShelfUseCase
from src.library.application.use_cases.restore_shelf import RestoreShelfUseCase
from src.library.application.use_cases.list_shelves import ListShelvesUseCase
from src.library.application.use_cases.add_book_to_shelf import AddBookToShelfUseCase
from src.library.application.use_cases.remove_book_from_shelf import RemoveBookFromShelfUseCase
from src.library.application.use_cases.reorder_shelf import ReorderShelfUseCase
from src.library.application.use_cases.get_shelf_books import GetShelfBooksUseCase
from src.library.infrastructure.services.stub_file_storage import StubFileStorageService
from src.library.infrastructure.sql.unit_of_work.library import SQLAlchemyLibraryUnitOfWork

# ---------------------------------------------------------------------------
# Infrastructure layer
# ---------------------------------------------------------------------------


def get_library_uow(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> SQLAlchemyLibraryUnitOfWork:
    return SQLAlchemyLibraryUnitOfWork(session_factory)


def get_file_storage() -> StubFileStorageService:
    return StubFileStorageService()


# Annotated aliases
LibraryUoWDep = Annotated[SQLAlchemyLibraryUnitOfWork, Depends(get_library_uow)]
FileStorageDep = Annotated[StubFileStorageService, Depends(get_file_storage)]

# ---------------------------------------------------------------------------
# Use-case providers — one function per use case
# ---------------------------------------------------------------------------


def get_create_book_use_case(
    uow: LibraryUoWDep,
) -> CreateBookUseCase:
    return CreateBookUseCase(uow=uow)  # type: ignore


def get_update_book_metadata_use_case(
    uow: LibraryUoWDep,
) -> UpdateBookMetadataUseCase:
    return UpdateBookMetadataUseCase(uow=uow)  # type: ignore


def get_upload_book_file_use_case(
    uow: LibraryUoWDep,
    file_storage: FileStorageDep,
) -> UploadBookFileUseCase:
    return UploadBookFileUseCase(uow=uow, file_storage=file_storage)  # type: ignore


def get_upload_book_cover_use_case(
    uow: LibraryUoWDep,
    file_storage: FileStorageDep,
) -> UploadBookCoverUseCase:
    return UploadBookCoverUseCase(uow=uow, file_storage=file_storage)  # type: ignore


def get_star_book_use_case(
    uow: LibraryUoWDep,
) -> StarBookUseCase:
    return StarBookUseCase(uow=uow)  # type: ignore


def get_delete_book_use_case(
    uow: LibraryUoWDep,
) -> DeleteBookUseCase:
    return DeleteBookUseCase(uow=uow)  # type: ignore


def get_restore_book_use_case(
    uow: LibraryUoWDep,
) -> RestoreBookUseCase:
    return RestoreBookUseCase(uow=uow)  # type: ignore


def get_search_books_use_case(
    uow: LibraryUoWDep,
) -> SearchBooksUseCase:
    return SearchBooksUseCase(uow=uow)  # type: ignore


def get_create_shelf_use_case(
    uow: LibraryUoWDep,
) -> CreateShelfUseCase:
    return CreateShelfUseCase(uow=uow)  # type: ignore


def get_update_shelf_use_case(
    uow: LibraryUoWDep,
) -> UpdateShelfUseCase:
    return UpdateShelfUseCase(uow=uow)  # type: ignore


def get_star_shelf_use_case(
    uow: LibraryUoWDep,
) -> StarShelfUseCase:
    return StarShelfUseCase(uow=uow)  # type: ignore


def get_delete_shelf_use_case(
    uow: LibraryUoWDep,
) -> DeleteShelfUseCase:
    return DeleteShelfUseCase(uow=uow)  # type: ignore


def get_restore_shelf_use_case(
    uow: LibraryUoWDep,
) -> RestoreShelfUseCase:
    return RestoreShelfUseCase(uow=uow)  # type: ignore


def get_list_shelves_use_case(
    uow: LibraryUoWDep,
) -> ListShelvesUseCase:
    return ListShelvesUseCase(uow=uow)  # type: ignore


def get_add_book_to_shelf_use_case(
    uow: LibraryUoWDep,
) -> AddBookToShelfUseCase:
    return AddBookToShelfUseCase(uow=uow)  # type: ignore


def get_remove_book_from_shelf_use_case(
    uow: LibraryUoWDep,
) -> RemoveBookFromShelfUseCase:
    return RemoveBookFromShelfUseCase(uow=uow)  # type: ignore


def get_reorder_shelf_use_case(
    uow: LibraryUoWDep,
) -> ReorderShelfUseCase:
    return ReorderShelfUseCase(uow=uow)  # type: ignore


def get_get_shelf_books_use_case(
    uow: LibraryUoWDep,
) -> GetShelfBooksUseCase:
    return GetShelfBooksUseCase(uow=uow)  # type: ignore