from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: add DB table creation, cache warm-up, etc. here
    yield
    # Shutdown: close DB connections, flush queues, etc. here
