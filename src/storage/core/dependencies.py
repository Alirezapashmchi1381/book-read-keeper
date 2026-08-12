from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.dependencies.database import get_session_factory
from src.storage.application.use_cases.upload_object import UploadObjectUseCase
from src.storage.application.use_cases.download_object import DownloadObjectUseCase
from src.storage.application.use_cases.delete_object import DeleteObjectUseCase
from src.storage.application.use_cases.get_object import GetObjectUseCase
from src.storage.application.use_cases.list_objects import ListObjectsUseCase
from src.storage.infrastructure.services.s3_file_storage import S3Config, S3FileStorageService
from src.storage.infrastructure.sql.unit_of_work.storage import SQLAlchemyStorageUnitOfWork

# ---------------------------------------------------------------------------
# Infrastructure layer
# ---------------------------------------------------------------------------


def get_storage_uow(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> SQLAlchemyStorageUnitOfWork:
    return SQLAlchemyStorageUnitOfWork(session_factory)


def get_file_storage() -> S3FileStorageService:
    # TODO: read from settings once S3 config is added to Settings.
    config = S3Config(bucket="book-read-keeper")
    return S3FileStorageService(config)


# Annotated aliases
StorageUoWDep = Annotated[SQLAlchemyStorageUnitOfWork, Depends(get_storage_uow)]
FileStorageDep = Annotated[S3FileStorageService, Depends(get_file_storage)]

# ---------------------------------------------------------------------------
# Use-case providers — one function per use case
# ---------------------------------------------------------------------------


def get_upload_object_use_case(
    uow: StorageUoWDep,
    file_storage: FileStorageDep,
) -> UploadObjectUseCase:
    return UploadObjectUseCase(uow=uow, file_storage=file_storage)  # type: ignore


def get_download_object_use_case(
    uow: StorageUoWDep,
    file_storage: FileStorageDep,
) -> DownloadObjectUseCase:
    return DownloadObjectUseCase(uow=uow, file_storage=file_storage)  # type: ignore


def get_delete_object_use_case(
    uow: StorageUoWDep,
    file_storage: FileStorageDep,
) -> DeleteObjectUseCase:
    return DeleteObjectUseCase(uow=uow, file_storage=file_storage)  # type: ignore


def get_get_object_use_case(
    uow: StorageUoWDep,
) -> GetObjectUseCase:
    return GetObjectUseCase(uow=uow)  # type: ignore


def get_list_objects_use_case(
    uow: StorageUoWDep,
) -> ListObjectsUseCase:
    return ListObjectsUseCase(uow=uow)  # type: ignore