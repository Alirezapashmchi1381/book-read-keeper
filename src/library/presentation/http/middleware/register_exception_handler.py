from fastapi import FastAPI

from src.library.domain.exceptions import (
    BookNotFoundError,
    ShelfNotFoundError,
    BookNotInShelfError,
    DuplicateBookInShelfError,
    ShelfLimitExceededError,
    BookAlreadyDeletedError,
    BookNotDeletedError,
    ShelfAlreadyDeletedError,
    ShelfNotDeletedError,
    FileStorageError,
    InvalidFileError,
    LibraryError,
    ResourceCorruptedError,
)

from src.library.presentation.http.exception_handlers import (
    book_not_found_handler,
    shelf_not_found_handler,
    book_not_in_shelf_handler,
    conflict_handler,
    bad_request_handler,
    resource_corrupted_handler,
    library_error_handler,
    unhandled_error_handler,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BookNotFoundError, book_not_found_handler)
    app.add_exception_handler(ShelfNotFoundError, shelf_not_found_handler)
    app.add_exception_handler(BookNotInShelfError, book_not_in_shelf_handler)
    app.add_exception_handler(DuplicateBookInShelfError, conflict_handler)
    app.add_exception_handler(ShelfLimitExceededError, conflict_handler)
    app.add_exception_handler(BookAlreadyDeletedError, conflict_handler)
    app.add_exception_handler(BookNotDeletedError, conflict_handler)
    app.add_exception_handler(ShelfAlreadyDeletedError, conflict_handler)
    app.add_exception_handler(ShelfNotDeletedError, conflict_handler)
    app.add_exception_handler(FileStorageError, bad_request_handler)
    app.add_exception_handler(InvalidFileError, bad_request_handler)
    app.add_exception_handler(ResourceCorruptedError, resource_corrupted_handler)
    app.add_exception_handler(LibraryError, library_error_handler)
    app.add_exception_handler(ValueError, library_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)