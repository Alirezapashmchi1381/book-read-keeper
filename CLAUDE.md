# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

book-read-keeper is a backend service that tracks every reading activity a user performs on books (annotations, progress, library management). The project is in early development.

## Architecture

The codebase follows Domain-Driven Design (DDD) with hexagonal architecture, organized by bounded context under `src/`:

- `identity` - user accounts, authentication, refresh tokens
- `library` - book collection management
- `reader` - reading sessions and progress tracking
- `annotations` - highlights, notes, bookmarks
- `storage` - file/blob storage abstraction
- `api` - HTTP layer (FastAPI expected)
- `shared` - cross-cutting value objects and utilities

Each bounded context follows a strict four-layer structure:

```
src/{context}/
  domain/
    entities/       # Aggregate roots and entities (pure Python dataclasses)
    value_objects/  # Immutable, validated value objects (frozen dataclasses)
    ports/          # Repository interfaces defined as typing.Protocol
  application/      # Use cases / command and query handlers
  presentation/     # Controllers, serializers, HTTP schemas
  repository/       # Infrastructure implementations of domain ports
```

Imports use the `src.` prefix (e.g., `from src.identity.domain.entities.user import User`). Run Python from the project root so `src` is on the path.

## Conventions

- Repositories are split into query (read) and command (write) protocols, defined in `domain/ports/`.
- Value objects raise `ValueError` in `__post_init__` when invariants are violated.
- Domain entities carry no infrastructure dependencies; persistence is injected via port interfaces.
- The `identity` bounded context is the only one with code so far; others are stubs.

## Environment

Python venv at `.venv/`. No packages beyond pip are installed yet. Activate with:

```bash
source .venv/bin/activate
```

No build scripts, test runner, or linter are configured yet. When adding them, prefer `pyproject.toml` as the single config file.
