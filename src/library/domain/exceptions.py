class LibraryError(Exception):
    """Base class for library domain errors."""


class BookNotFoundError(LibraryError):
    """Raised when a book does not exist."""


class ShelfNotFoundError(LibraryError):
    """Raised when a shelf does not exist."""


class DuplicateBookInShelfError(LibraryError):
    """Raised when a book is already in a shelf."""


class BookNotInShelfError(LibraryError):
    """Raised when a book is not in a shelf."""


class ShelfLimitExceededError(LibraryError):
    """Raised when a shelf would exceed its maximum capacity."""


class BookAlreadyDeletedError(LibraryError):
    """Raised when trying to delete an already deleted book."""


class BookNotDeletedError(LibraryError):
    """Raised when trying to restore a book that is not deleted."""


class ShelfAlreadyDeletedError(LibraryError):
    """Raised when trying to delete an already deleted shelf."""


class ShelfNotDeletedError(LibraryError):
    """Raised when trying to restore a shelf that is not deleted."""


class FileStorageError(LibraryError):
    """Raised when a file storage operation fails."""


class InvalidFileError(LibraryError):
    """Raised when an uploaded file is invalid (wrong format, too large, etc.)."""


class ResourceCorruptedError(LibraryError):
    """Raised when an entity is in an unexpected or inconsistent state."""
