# book-read-keeper

**book-read-keeper** is a backend for reading books syncytially — in sync across your devices — while recording every activity you perform. Reading position, highlights, notes, and library organization are all tracked so that wherever you stop, you can resume exactly where you left off.

The Architecture of this project is a **modular monolith** built with **FastAPI** and **Clean Architecture**. Each module (identity, library, annotations, reader, storage) is a self-contained, potentially independent service with its own domain, application, infrastructure, and presentation layers. All cross-cutting concerns — the database engine, session factory, and settings — are provided once, centrally in `src/core/`, via FastAPI's dependency injection.

Every module exposes its own FastAPI sub-app factory that the root app mounts under a path prefix (for example `/identity` and `/library`). Dependencies flow from the shared `src/core/` composition root into each module's `core/dependencies.py`, where infrastructure implementations are assembled into use cases and injected into routers.

Modules: **identity** (signup, login, JWT + refresh tokens, email and password handling) is implemented; **library** (books, shelves, metadata) is in progress; **annotations** (highlights and notes on book text) has its domain layer completed; **reader** (syncytical reading progress) and **storage** (book file storage) are stubs.

The backend runs on Python 3.12+ with FastAPI, SQLAlchemy 2.0 async, and Alembic. Configuration comes from an environment file (default `.env.dev`).
