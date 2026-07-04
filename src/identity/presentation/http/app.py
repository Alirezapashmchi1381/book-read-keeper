from fastapi import FastAPI

from src.identity.presentation.http.api.v1.router import v1_router
from src.identity.presentation.http.exception_handlers import (
    unhandled_error_handler,
    value_error_handler,
)
from src.identity.presentation.http.middleware.cors import add_cors


def create_app(allowed_origins: list[str] | None = None) -> FastAPI:
    app = FastAPI(title="Book Read Keeper — Identity API")

    add_cors(app, allowed_origins=allowed_origins or ["*"])

    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)

    app.include_router(v1_router, prefix="/api")

    return app
