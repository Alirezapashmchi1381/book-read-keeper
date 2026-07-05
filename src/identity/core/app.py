from fastapi import FastAPI

from src.identity.presentation.http.middleware.register_exception_handler import register_exception_handlers
from src.core.config import get_settings
from src.core.lifespan import lifespan
from src.identity.presentation.http.api.v1.router import v1_router as identity_v1_router
from src.identity.domain.exceptions import (
    AuthenticationError,
    ConflictError,
    DomainError,
    InvalidTokenError,
    NotFoundError,
)
from src.identity.presentation.http.exception_handlers import (
    authentication_error_handler,
    conflict_error_handler,
    domain_error_handler,
    invalid_token_error_handler,
    not_found_error_handler,
    unhandled_error_handler,
    value_error_handler,
)
from src.identity.presentation.http.middleware.cors import add_cors


def create_identity_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Book Read Keeper identity",
        version="1.0.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    add_cors(app, settings.cors_origins)
    register_exception_handlers(app)

    # Bounded contexts
    app.include_router(identity_v1_router, prefix="/api")
    # app.include_router(library_v1_router, prefix="/api")   # add when ready
    # app.include_router(reader_v1_router, prefix="/api")

    return app


app = create_identity_app()
