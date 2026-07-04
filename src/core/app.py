from fastapi import FastAPI

from src.core.config import get_settings
from src.core.lifespan import lifespan
from src.identity.presentation.http.api.v1.router import v1_router as identity_v1_router
from src.identity.presentation.http.exception_handlers import value_error_handler
from src.identity.presentation.http.middleware.cors import add_cors


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Book Read Keeper",
        version="1.0.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    add_cors(app, settings.cors_origins)

    app.add_exception_handler(ValueError, value_error_handler)

    # Bounded contexts
    app.include_router(identity_v1_router, prefix="/api")
    # app.include_router(library_v1_router, prefix="/api")   # add when ready
    # app.include_router(reader_v1_router, prefix="/api")

    return app


app = create_app()
