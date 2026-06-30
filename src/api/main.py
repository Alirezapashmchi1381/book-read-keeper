from fastapi import FastAPI

from src.identity.presentation.routes import router as identity_router

app = FastAPI(title="Book Read Keeper")

app.include_router(identity_router, prefix="/api/v1")
