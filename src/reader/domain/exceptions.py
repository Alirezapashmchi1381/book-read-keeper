class ReaderError(Exception):
    """Base class for reader domain errors."""


class ReadingSessionNotFoundError(ReaderError):
    """Raised when a reading session does not exist."""


class SessionAlreadyExistsError(ReaderError):
    """Raised when a session already exists for a (user, book) pair."""


class InvalidProgressError(ReaderError):
    """Raised when progress percent is outside 0.0–100.0."""


class InvalidLocatorError(ReaderError):
    """Raised when a locator is invalid."""