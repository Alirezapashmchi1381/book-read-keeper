class StorageError(Exception):
    """Base class for storage domain errors."""


class BucketNotFoundError(StorageError):
    """Raised when a bucket does not exist."""


class ObjectNotFoundError(StorageError):
    """Raised when an object does not exist."""


class BucketLimitExceededError(StorageError):
    """Raised when a bucket would exceed its max objects or max size."""


class BucketAlreadyExistsError(StorageError):
    """Raised when trying to create a bucket with a name that already exists."""


class ObjectAlreadyExistsError(StorageError):
    """Raised when trying to create an object with a key that already exists."""



class ObjectNotDeletedError(StorageError):
    """Raised when trying to restore an object that is not deleted."""


class InvalidBucketNameError(StorageError):
    """Raised when a bucket name is invalid."""


class InvalidObjectKeyError(StorageError):
    """Raised when an object key is invalid."""


class InvalidStorageClassError(StorageError):
    """Raised when an invalid storage class is specified."""