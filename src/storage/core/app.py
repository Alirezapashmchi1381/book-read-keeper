from fastapi import FastAPI


def create_storage_app() -> FastAPI:
    app = FastAPI()
    # Presentation layer (HTTP API) is not yet implemented.
    return app