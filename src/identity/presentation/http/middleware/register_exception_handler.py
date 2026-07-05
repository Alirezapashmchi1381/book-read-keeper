from fastapi import FastAPI

from src.identity.domain.exceptions import (
    AuthenticationError,
    ConflictError,
    DomainError,
    InvalidTokenError,
    NotFoundError,
)

from src.identity.presentation.http.exception_handlers import (
    domain_error_handler,
    not_found_error_handler,
    conflict_error_handler,
    authentication_error_handler,
    invalid_token_error_handler,
    value_error_handler,
    unhandled_error_handler
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(ConflictError, conflict_error_handler)
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(InvalidTokenError, invalid_token_error_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)