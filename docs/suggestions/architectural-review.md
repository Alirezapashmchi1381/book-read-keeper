# Architectural Review — book-read-keeper

> DDD + Hexagonal Architecture audit of the `identity` bounded context.
> All other contexts (`library`, `reader`, `annotations`, `storage`) are stubs and excluded.

---

## What Is Already Good

Before the problems: several things are done correctly and should be kept.

- **Hexagonal structure is real.** Domain entities carry zero infrastructure imports. Ports are `typing.Protocol`. Infrastructure implements the ports without the domain knowing it. The dependency arrow consistently points inward.
- **Command/Query split on repositories.** `UserCommandRepository` / `UserQueryRepository` separation is clean CQRS at the persistence boundary. This makes read and write concerns independently evolvable.
- **Unit of Work pattern is sound.** The `SQLAlchemyUnitOfWork` base class is a clean async context manager. Auto-commit on success and rollback on exception is implemented correctly.
- **Pure use cases.** Every use case is a plain `@dataclass` with an `execute()` method. No framework coupling, no HTTP concepts, trivially testable.
- **Test double strategy is excellent.** `FakeIdentityUnitOfWork`, `FakePasswordHasher`, etc. implement the same duck-typed protocols as the real infrastructure. Use-case tests run in-memory with zero I/O.
- **Token rotation on refresh.** `RefreshTokenUseCase` revokes the old token and issues a new one — correct security practice.
- **Sending email outside the UoW.** `RequestEmailVerificationUseCase` closes the UoW transaction first, then calls `email_service.send_email_verification()`. This avoids holding a DB transaction open during a network call.

---

## Problems and Improvement Suggestions

### 1. Anemic Domain Model — Business Logic Leaking into Use Cases

**Problem.**
The `User` entity only has `activate()`, `deactivate()`, and `verify()` — lifecycle state transitions.
Password mutation happens directly from application code:

```python
# change_password.py — application layer
user.password_hash = self.password_hasher.hash(dto.new_password)
await uow.users.command.save(user)
```

This is an anemic domain model. The application layer is making a domain decision (what it means to change a password) instead of delegating it to the aggregate.

**Fix.**
Put the behaviour where the invariants live — on the entity:

```python
# User entity
def change_password(self, hasher: PasswordHasher, current: str, new: str) -> None:
    if not hasher.verify(current, self.password_hash):
        raise ValueError("Current password is incorrect")
    self.password_hash = hasher.hash(new)
    self.updated_at = datetime.now()
```

The use case then becomes orchestration-only:

```python
user.change_password(self.password_hasher, dto.current_password, dto.new_password)
await uow.users.command.save(user)
```

The same pattern applies to `ResetPasswordUseCase` — it assigns `user.password_hash` directly.

---

### 2. Token Entities Are Not Proper Aggregates — Inconsistent Identity Types

**Problem.**
`RefreshToken`, `EmailVerificationToken`, and `PasswordResetToken` use raw `UUID` for `user_id`:

```python
@dataclass
class RefreshToken:
    user_id: UUID   # raw UUID
```

But `User` uses a typed value object:

```python
@dataclass
class User:
    id: UserId      # value object
```

This inconsistency means the domain cannot express the relationship between a token and a user with type safety. You can accidentally pass any `UUID` where a `UserId` is expected.

**Fix.**
Use `UserId` consistently on all entities that reference a user:

```python
@dataclass
class RefreshToken:
    user_id: UserId
```

---

### 3. `PasswordHasher` Is Misused for Token Hashing

**Problem.**
Refresh tokens, email verification tokens, and password reset tokens are all hashed using `PasswordHasher`:

```python
token_hash=self.password_hasher.hash(raw_refresh_token)
```

`PasswordHasher` is implemented by `BcryptPasswordHasher`. Bcrypt is intentionally slow (cost factor ~12). Hashing a random 32-byte token with bcrypt is both semantically wrong and a performance problem — bcrypt is designed for low-entropy human passwords, not for cryptographically random tokens.

Random tokens should be stored as HMAC-SHA256 hashes, which are fast and appropriate.

**Fix.**
Introduce a separate port:

```python
class TokenHasher(Protocol):
    def hash(self, token: str) -> str: ...
    def verify(self, token: str, hashed: str) -> bool: ...
```

Implement it with HMAC-SHA256. Use `PasswordHasher` only for passwords. Use `TokenHasher` for all opaque random tokens. This distinction is a domain concept — the port boundary makes it explicit.

---

### 4. `TokenService` Port Is Semantically Wrong

**Problem.**
`TokenService` has two methods:

```python
class TokenService(Protocol):
    def generate_access_token(self, user_id: UUID) -> str: ...
    def generate_refresh_token(self) -> str: ...
```

`generate_refresh_token()` doesn't actually generate a JWT or a structured token — it generates a random URL-safe string (`secrets.token_urlsafe(32)`). It's reused in `RequestEmailVerificationUseCase` to generate email verification tokens too:

```python
raw_token = self.token_service.generate_refresh_token()  # generating an email token!
```

The naming is misleading and the abstraction is leaking implementation details.

**Fix.**
Split into two ports. `TokenService` handles structured JWT tokens. A separate `SecretGenerator` (or `OpaqueTokenGenerator`) handles random secret generation:

```python
class TokenService(Protocol):
    def generate_access_token(self, user_id: UUID) -> str: ...
    def verify_access_token(self, token: str) -> UUID: ...  # also missing — see #5

class SecretGenerator(Protocol):
    def generate(self) -> str: ...
```

---

### 5. Access Token Verification Has No Domain Port

**Problem.**
JWT decoding happens directly in `src/core/dependencies/auth.py`, a FastAPI dependency:

```python
payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[...])
```

There is no `TokenService.verify_access_token()` method. The verification logic is duplicated infrastructure code outside the domain, not behind a port. If you ever want to test authenticated endpoints without a real JWT, you have no seam to inject.

**Fix.**
Add `verify_access_token(token: str) -> UUID` to the `TokenService` port. The `auth.py` dependency calls `token_service.verify_access_token()` rather than importing `jwt` directly. This also means the `core/dependencies/auth.py` logic can take a `TokenService` via DI.

---

### 6. Domain Errors Are Untyped `ValueError`

**Problem.**
Every business rule violation raises a generic `ValueError`:

```python
raise ValueError("Email is already registered")
raise ValueError("Invalid credentials")
raise ValueError("User not found")
raise ValueError("Invalid or expired reset token")
```

The exception handler converts all `ValueError` to HTTP 400. But these are semantically different:
- `"User not found"` should be 404.
- `"Invalid credentials"` should stay 401.
- `"Email is already registered"` should be 409 Conflict.

Currently they all collapse to 400, which is incorrect HTTP semantics.

**Fix.**
Create a typed exception hierarchy in `src/identity/domain/exceptions.py`:

```python
class DomainError(Exception): ...
class NotFoundError(DomainError): ...
class ConflictError(DomainError): ...
class AuthenticationError(DomainError): ...
class InvalidTokenError(DomainError): ...
```

Map them to HTTP status codes in `exception_handlers.py`. Use cases raise typed exceptions; the HTTP layer translates them. This keeps the domain ignorant of HTTP while giving the API correct status codes.

---

### 7. Missing `Username` Value Object

**Problem.**
`username` is a raw `str` everywhere — in `User`, in DTOs, in queries. There is no validation of length, allowed characters, or format. The project already validates `Email` with a value object; `Username` deserves the same treatment.

**Fix.**

```python
@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self):
        if not 3 <= len(self.value) <= 30:
            raise ValueError("Username must be 3–30 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', self.value):
            raise ValueError("Username may only contain letters, digits, and underscores")
```

---

### 8. Naive `datetime.now()` — Timezone Inconsistency

**Problem.**
All entities and use cases use `datetime.now()` (timezone-naive):

```python
created_at: datetime = field(default_factory=datetime.now)
expires_at=datetime.now() + timedelta(days=REFRESH_TOKEN_TTL_DAYS)
```

But `JWTTokenService` correctly uses:

```python
datetime.now(timezone.utc)
```

Comparing a naive `datetime` with an aware `datetime` raises a `TypeError` at runtime. The JWT `exp` claim uses UTC; comparing it against a naive `datetime.now()` token expiry is an implicit inconsistency that will manifest as bugs when you add any timezone-aware timestamp logic.

**Fix.**
Replace all `datetime.now()` with `datetime.now(timezone.utc)` across all entities and use cases. Make it a project rule: all datetimes are UTC-aware.

---

### 9. UoW Sub-UoW Nesting Is Non-Standard and Confusing

**Problem.**
The UoW design introduces a nested level: `IdentityUnitOfWork → UserUoW → query/command`. This is non-standard. The canonical UoW pattern exposes repositories directly:

```python
# Standard
uow.users.find_by_email(...)  # uow.users is a repository

# Current design (nested)
uow.users.query.find_by_email(...)  # uow.users is a sub-UoW containing repos
```

The sub-UoW objects (`UserUoW`, `RefreshTokenUoW`, etc.) in `domain/ports/unit_of_work.py` add a layer without adding behaviour. They are not context managers themselves and don't commit or rollback — they just group `query` and `command` repositories.

**Fix.**
Consider flattening: expose `user_queries`, `user_commands`, `refresh_token_queries`, etc. directly on `IdentityUnitOfWork`, or collapse each pair into a single `UserRepository` that exposes both read and write methods. The current nested structure makes callers write `uow.users.query.find_by_id(...)` where `uow.user_queries.find_by_id(...)` would be cleaner.

---

### 10. `UserTransformer.to_model()` Always Creates a New SQLAlchemy Object

**Problem.**
Every `save()` call creates a new `UserModel` and passes it to `session.merge()`:

```python
async def save(self, user: User) -> None:
    model = UserTransformer.to_model(user)
    await self._session.merge(model)
```

`session.merge()` works correctly here because SQLAlchemy detects the primary key and performs an upsert. However, every call allocates a new ORM object and forces SQLAlchemy to do a SELECT before the UPDATE to resolve the identity map. For high-frequency saves this is inefficient.

**Fix.**
For updates, use a targeted `UPDATE` statement rather than `merge()`:

```python
await self._session.execute(
    update(UserModel)
    .where(UserModel.id == entity.id.value)
    .values(email=entity.email.address, is_active=entity.is_active, ...)
)
```

Or use SQLAlchemy's session tracking by fetching the model first, modifying it in place, and letting the session auto-flush.

---

### 11. No Domain Events

**Problem.**
When a user signs up, verifies their email, or is deactivated, nothing is published. The other bounded contexts (`library`, `reader`) will eventually need to react to identity events. Without domain events, these contexts must be coupled directly to `identity` or poll the database.

**Fix.**
Introduce a simple domain event pattern:

```python
# domain/events.py
@dataclass(frozen=True)
class UserRegistered:
    user_id: UserId
    email: str
    occurred_at: datetime

@dataclass(frozen=True)
class UserVerified:
    user_id: UserId
    occurred_at: datetime
```

Entities collect events; the UoW dispatches them after commit. Start with an in-process event bus; replace with a message broker later without changing the domain.

---

### 12. Stub Bounded Contexts Contain Invalid Placeholder Files

**Problem.**
`src/annotations/1`, `src/library/1`, `src/reader/1`, `src/shared/1`, `src/storage/1` are files literally named `1`. This appears to be an editor artifact.

**Fix.**
Replace each with `__init__.py` so Python treats them as packages. Add a `README.md` stub or at minimum a comment explaining the planned structure.

---

### 13. `src/core/` Is an Undocumented Fifth Layer

**Problem.**
`src/core/` holds `config.py`, `lifespan.py`, and all DI providers (`dependencies/`). It is not part of the four-layer model described in `CLAUDE.md` and acts as a cross-cutting infrastructure container. The presentation layer's `dependencies.py` is a thin re-export of `src.core.dependencies.*` — a pure indirection layer with no logic.

**Fix.**
Document `src/core/` in `CLAUDE.md` as the "composition root" or "bootstrap layer". Consider collapsing `src/identity/presentation/http/dependencies.py` (which is just re-exports) into the routers' direct imports of `src.core.dependencies.identity`.

---

### 14. No Input Validation at Application Boundary

**Problem.**
`SignupInputDto` is a frozen dataclass with raw strings:

```python
@dataclass(frozen=True)
class SignupInputDto:
    email: str
    username: str
    password: str
```

The `Email` value object validates on construction inside the use case. But password strength (minimum length, complexity) and username format are never validated. A caller can pass an empty string or a 1-character password and the domain will accept it.

**Fix.**
Either validate in the DTO (turn DTOs into Pydantic models) or enforce in the domain entity's `create()` factory method. The domain should be the last line of defence, but the DTO layer should be the first. Both are appropriate places; choose one and apply it consistently.

---

## Priority Order

| # | Issue | Severity | Effort |
|---|-------|----------|--------|
| 6 | Untyped `ValueError` → wrong HTTP status codes | High | Low |
| 8 | Naive `datetime.now()` | High | Low |
| 3 | Bcrypt for token hashing | High | Medium |
| 1 | Anemic domain (password logic in use case) | Medium | Low |
| 4 | `TokenService` semantic mismatch | Medium | Medium |
| 5 | No `verify_access_token` port | Medium | Medium |
| 2 | `UUID` vs `UserId` inconsistency on token entities | Medium | Low |
| 7 | Missing `Username` value object | Medium | Low |
| 14 | No input validation on DTOs | Medium | Low |
| 11 | No domain events | Low | High |
| 9 | Sub-UoW nesting ergonomics | Low | Medium |
| 10 | `merge()` inefficiency | Low | Medium |
| 12 | Stub `1` files | Low | Trivial |
| 13 | `src/core/` undocumented | Low | Trivial |
