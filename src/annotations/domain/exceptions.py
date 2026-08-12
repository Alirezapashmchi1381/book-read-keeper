class AnnotationsError(Exception):
    """Base class for annotations domain errors."""


class HighlightNotFoundError(AnnotationsError):
    """Raised when a highlight does not exist."""


class HighlightAlreadyDeletedError(AnnotationsError):
    """Raised when trying to delete an already deleted highlight."""


class HighlightNotDeletedError(AnnotationsError):
    """Raised when trying to restore a highlight that is not deleted."""


class InvalidLocatorError(AnnotationsError):
    """Raised when a locator is invalid (missing/inconsistent fields)."""


class SelectionRangeError(AnnotationsError):
    """Raised when the selection range (start/end locator) is invalid."""