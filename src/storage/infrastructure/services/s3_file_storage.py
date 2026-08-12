from dataclasses import dataclass

import aioboto3

from src.storage.domain.ports.file_storage_service import FileStorageService
from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass


@dataclass(frozen=True)
class S3Config:
    bucket: str
    region: str = "us-east-1"
    endpoint_url: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None


class S3FileStorageService(FileStorageService):
    """S3-backed file storage implemented with aioboto3."""

    def __init__(self, config: S3Config) -> None:
        self._config = config

    def _session(self) -> aioboto3.Session:
        return aioboto3.Session(
            aws_access_key_id=self._config.aws_access_key_id,
            aws_secret_access_key=self._config.aws_secret_access_key,
            region_name=self._config.region,
        )

    async def upload(
        self,
        key: ObjectKey,
        content: bytes,
        content_type: str,
        storage_class: StorageClass,
    ) -> Etag:
        session = self._session()
        async with session.client(
            "s3",
            endpoint_url=self._config.endpoint_url,
        ) as s3:
            response = await s3.put_object(
                Bucket=self._config.bucket,
                Key=key._value,
                Body=content,
                ContentType=content_type,
                StorageClass=storage_class.name,
            )
            etag = response.get("ETag", "").strip('"')
            return Etag(etag)

    async def download(self, key: ObjectKey) -> bytes:
        session = self._session()
        async with session.client(
            "s3",
            endpoint_url=self._config.endpoint_url,
        ) as s3:
            response = await s3.get_object(
                Bucket=self._config.bucket,
                Key=key._value,
            )
            body = await response["Body"].read()
            return body

    async def delete(self, key: ObjectKey) -> None:
        session = self._session()
        async with session.client(
            "s3",
            endpoint_url=self._config.endpoint_url,
        ) as s3:
            await s3.delete_object(
                Bucket=self._config.bucket,
                Key=key._value,
            )

    async def get_presigned_url(self, key: ObjectKey, expires_in: int = 3600) -> str:
        session = self._session()
        async with session.client(
            "s3",
            endpoint_url=self._config.endpoint_url,
        ) as s3:
            url = await s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self._config.bucket,
                    "Key": key._value,
                },
                ExpiresIn=expires_in,
            )
            return url