from fastapi import FastAPI

from src.annotations.domain.exceptions import (
    AnnotationsError,
    HighlightNotFoundError,
    HighlightAlreadyDeletedError,
    HighlightNotDeletedError,
    InvalidLocatorError,
    SelectionRangeError,
)
from src.annotations.presentation.http.exception_handlers import (
    not_found_handler,
    conflict_handler,
    bad_request_handler,
    annotations_error_handler,
    unhandled_error_handler,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HighlightNotFoundError, not_found_handler)
    app.add_exception_handler(HighlightAlreadyDeletedError, conflict_handler)
    app.add_exception_handler(HighlightNotDeletedError, conflict_handler)
    app.add_exception_handler(InvalidLocatorError, bad_request_handler)
    app.add_exception_handler(SelectionRangeError, bad_request_handler)
    app.add_exception_handler(AnnotationsError, annotations_error_handler)
    app.add_exception_handler(ValueError, annotations_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)