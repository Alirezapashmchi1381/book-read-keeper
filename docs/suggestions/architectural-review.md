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

**Status: ✅ Fixed**

**Problem.**
The `User` entity only has `activate()`, `deactivate()`, `verify()`, and `verify_password()` — lifecycle state transitions and a password verification helper.
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
        raise AuthenticationError("Current password is incorrect")
    self.password_hash = hasher.hash(new)
    self.updated_at = datetime.now(timezone.utc)
```

The use case then becomes orchestration-only:

```python
user.change_password(self.password_hasher, dto.current_password, dto.new_password)
await uow.users.command.save(user)
```

The same pattern applies to `ResetPasswordUseCase` — it assigns `user.password_hash` directly.

---

### 2. Token Entities Are Not Proper Aggregates — Inconsistent Identity Types

**Status: ❌ Still open (UserId value object was removed, see discussion below)**

**Problem.**
`RefreshToken`, `EmailVerificationToken`, and `PasswordResetToken` use raw `UUID` for `user_id`:

```python
@dataclass
class RefreshToken:
    user_id: UUID   # raw UUID
```

And `User` also uses raw `UUID`:

```python
@dataclass
class User:
    id: UUID        # raw UUID — UserId value object was removed in commit 75b6ae6
```

> **Note:** The original review suggested a `UserId` value object, but commit `75b6ae6` (`refactor(identity-domain)delete value object UserID`) explicitly removed it. The domain chose to keep raw `UUID` for user identity across all entities. This is a valid simplification — `UUID` is already type-safe and self-validating — and the inconsistency is no longer present since `User` also uses raw `UUID`.

**Recommendation.**
`UUID` is now consistent across all entities. If you want stronger typing in the future, introduce a `UserId` value object and apply it everywhere. This is low priority.

---

### 3. `PasswordHasher` Is Misused for Token Hashing

**Status: ✅ Fixed (commits 7ff632d, dbb2447)**

**Changes Made.**
- A `TokenHasher` port was introduced (`src/identity/domain/ports/token_hasher.py`) with `hash()` and `verify()` methods.
- An `HMACTokenHasher` implementation was created (`src/identity/infrastructure/services/hmac_token_hasher.py`) using HMAC-SHA256.
- All use cases now depend on `TokenHasher` for hashing opaque tokens (refresh, verification, reset) instead of `PasswordHasher`.
- `PasswordHasher` (implemented by `BcryptPasswordHasher`) is now only used for human passwords.

**Result.**
Bcrypt (cost factor ~12) is no longer used for random 32-byte tokens. Token hashing uses fast HMAC-SHA256. This is both semantically correct and a performance improvement.

---

### 4. `TokenService` Port Is Semantically Wrong

**Status: ✅ Fixed (commit dbb2447)**

**Changes Made.**
- `TokenService` port (`src/identity/domain/ports/token_service.py`) now only handles structured JWT tokens: `generate_access_token()` and `verify_access_token()`.
- A separate `SecretGenerator` port (`src/identity/domain/ports/secret_generator.py`) was introduced with a single `generate()` method.
- `SecretsGenerator` (`src/identity/infrastructure/services/secrets_generator.py`) uses `secrets.token_urlsafe(32)` for generating opaque random tokens.
- All use cases that need random token generation (refresh, email verification, password reset) depend on `SecretGenerator`. None misuse `TokenService` for this purpose.

**Result.**
The naming is now accurate. `TokenService` = JWT tokens. `SecretGenerator` = cryptographically random opaque tokens.

---

### 5. Access Token Verification Has No Domain Port

**Status: ✅ Fixed**

**Changes Made.**
- `TokenService` port was extended with `verify_access_token(token: str) -> UUID` method.
- `JWTTokenService` implements it, encapsulating `jwt.decode()` behind the port.
- `get_current_user_id()` in `src/identity/core/dependencies.py` uses `token_service.verify_access_token()` rather than importing `jwt` directly.

**Result.**
JWT decoding is behind a port, making it mockable in tests. No infrastructure import leak in application or presentation code. The `jwt.decode()` call is only inside `JWTTokenService`.

---

### 6. Domain Errors Are Untyped `ValueError`

**Status: ✅ Fixed (commits db6f384, 5932415, a36a101)**

**Changes Made.**
- Created a typed exception hierarchy in `src/identity/domain/exceptions.py`:
  - `DomainError` — base class
  - `NotFoundError` — maps to HTTP 404
  - `ConflictError` — maps to HTTP 409
  - `AuthenticationError` — maps to HTTP 401
  - `InvalidTokenError` — maps to HTTP 401
- Registered exception handlers in `src/identity/presentation/http/exception_handlers.py`:
  - `not_found_error_handler` → 404
  - `conflict_error_handler` → 409
  - `authentication_error_handler` → 401
  - `invalid_token_error_handler` → 401
  - `domain_error_handler` → 400 (fallback for other domain errors)
  - `value_error_handler` → 400 (fallback for generic validation errors)
  - `unhandled_error_handler` → 500

**Result.**
Each business rule violation now has the correct HTTP status code:
- `NotFoundError` → 404
- `ConflictError` → 409
- `AuthenticationError` → 401
- Generic `DomainError` → 400

---

### 7. Missing `Username` Value Object

**Status: ❌ Still open**

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

**Status: ❌ Still open**

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

**Status: ❌ Still open**

**Problem.**
The UoW design introduces a nested level: `IdentityUnitOfWork → UserUoW → query/command`. This is non-standard. The canonical UoW pattern exposes repositories directly:

```python
# Standard
uow.users.find_by_email(...)  # uow.users is a repository

# Current design (nested)
uow.users.query.find_by_id(...)  # uow.users is a sub-UoW containing repos
```

The sub-UoW objects (`UserUoW`, `RefreshTokenUoW`, etc.) in `domain/ports/unit_of_work.py` add a layer without adding behaviour. They are not context managers themselves and don't commit or rollback — they just group `query` and `command` repositories.

**Fix.**
Consider flattening: expose `user_queries`, `user_commands`, `refresh_token_queries`, etc. directly on `IdentityUnitOfWork`, or collapse each pair into a single `UserRepository` that exposes both read and write methods. The current nested structure makes callers write `uow.users.query.find_by_id(...)` where `uow.user_queries.find_by_id(...)` would be cleaner.

---

### 10. `UserTransformer.to_model()` Always Creates a New SQLAlchemy Object

**Status: ❌ Still open**

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
    .where(UserModel.id == entity.id)
    .values(email=entity.email.address, is_active=entity.is_active, ...)
)
```

Or use SQLAlchemy's session tracking by fetching the model first, modifying it in place, and letting the session auto-flush.

**Note:** This only applies to `user` repository so far. The token repositories may have a similar pattern.

---

### 11. No Domain Events

**Status: ❌ Still open**

**Problem.**
When a user signs up, verifies their email, or is deactivated, nothing is published. The other bounded contexts (`library`, `reader`) will eventually need to react to identity events. Without domain events, these contexts must be coupled directly to `identity` or poll the database.

**Fix.**
Introduce a simple domain event pattern:

```python
# domain/events.py
@dataclass(frozen=True)
class UserRegistered:
    user_id: UUID
    email: str
    occurred_at: datetime

@dataclass(frozen=True)
class UserVerified:
    user_id: UUID
    occurred_at: datetime
```

Entities collect events; the UoW dispatches them after commit. Start with an in-process event bus; replace with a message broker later without changing the domain.

---

### 12. Stub Bounded Contexts Contain Invalid Placeholder Files

**Status: ❌ Still open**

**Problem.**
`src/annotations/1`, `src/library/1`, `src/reader/1`, `src/shared/1`, `src/storage/1` are files literally named `1`. This appears to be an editor artifact.

**Fix.**
Replace each with `__init__.py` so Python treats them as packages. Add a `README.md` stub or at minimum a comment explaining the planned structure.

---

### 13. `src/core/` Is an Undocumented Fifth Layer

**Status: ❌ Still open**

**Problem.**
`src/core/` holds `config.py`, `lifespan.py`, and all DI providers (`dependencies/`). It is not part of the four-layer model described in `CLAUDE.md` and acts as a cross-cutting infrastructure container. The presentation layer's `dependencies.py` was previously a thin re-export of `src.core.dependencies.*` — a pure indirection layer with no logic.

**Note:** `src/identity/presentation/http/dependencies.py` no longer exists as a separate file; DI is handled directly in `src/identity/core/dependencies.py`. However, `src/core/` itself remains undocumented.

**Fix.**
Document `src/core/` in `CLAUDE.md` as the "composition root" or "bootstrap layer". Consider whether the split between `src/core/dependencies/` and `src/identity/core/dependencies.py` is still necessary, or if they should be consolidated.

---

### 14. No Input Validation at Application Boundary

**Status: ❌ Still open**

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

| # | Issue | Severity | Effort | Status |
|---|-------|----------|--------|--------|
| 6 | Untyped `ValueError` → wrong HTTP status codes | High | Low | ✅ Fixed |
| 8 | Naive `datetime.now()` | High | Low | ❌ Open |
| 3 | Bcrypt for token hashing | High | Medium | ✅ Fixed |
| 1 | Anemic domain (password logic in use case) | Medium | Low | ✅ Fixed |
| 4 | `TokenService` semantic mismatch | Medium | Medium | ✅ Fixed |
| 5 | Missing `verify_access_token` port | Medium | Medium | ✅ Fixed |
| 2 | `UUID` vs `UserId` inconsistency on token entities | Medium | Low | ⚠️ Resolved (UserId removed) |
| 7 | Missing `Username` value object | Medium | Low | ❌ Open |
| 14 | No input validation on DTOs | Medium | Low | ❌ Open |
| 11 | No domain events | Low | High | ❌ Open |
| 9 | Sub-UoW nesting ergonomics | Low | Medium | ❌ Open |
| 10 | `merge()` inefficiency | Low | Medium | ❌ Open |
| 12 | Stub `1` files | Low | Trivial | ❌ Open |
| 13 | `src/core/` undocumented | Low | Trivial | ❌ Open |
