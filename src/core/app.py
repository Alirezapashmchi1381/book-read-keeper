from fastapi import FastAPI

from src.core.config import get_settings
from src.core.lifespan import lifespan
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
from src.identity.core.app import create_identity_app
from src.library.core.app import create_library_app
from src.annotations.core.app import create_annotations_app
from src.reader.core.app import create_reader_app

def create_app() -> FastAPI:
    settings = get_settings()

    main_app = FastAPI(
        title="Book Read Keeper",
        version="1.0.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    add_cors(main_app, settings.cors_origins)

    main_app.mount("/identity", create_identity_app())
    main_app.mount("/library", create_library_app())
    main_app.mount("/annotations", create_annotations_app())
    main_app.mount("/reader", create_reader_app())

    return main_app


app = create_app()
