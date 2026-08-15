from fastapi import FastAPI

from src.reader.domain.exceptions import (
    ReaderError,
    ReadingSessionNotFoundError,
    SessionAlreadyExistsError,
    InvalidProgressError,
    InvalidLocatorError,
)
from src.reader.presentation.http.exception_handlers import (
    not_found_handler,
    conflict_handler,
    bad_request_handler,
    reader_error_handler,
    unhandled_error_handler,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ReadingSessionNotFoundError, not_found_handler)
    app.add_exception_handler(SessionAlreadyExistsError, conflict_handler)
    app.add_exception_handler(InvalidProgressError, bad_request_handler)
    app.add_exception_handler(InvalidLocatorError, bad_request_handler)
    app.add_exception_handler(ReaderError, reader_error_handler)
    app.add_exception_handler(ValueError, reader_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)