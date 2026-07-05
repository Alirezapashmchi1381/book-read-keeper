class DomainError(Exception):
    """Base class for identity domain errors."""


class NotFoundError(DomainError):
    """Raised when a requested resource does not exist."""


class ConflictError(DomainError):
    """Raised when an operation conflicts with existing state."""


class AuthenticationError(DomainError):
    """Raised when credentials are missing or invalid."""


class InvalidTokenError(DomainError):
    """Raised when a token is malformed, expired, or otherwise invalid."""
