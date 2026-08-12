from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass
from src.storage.infrastructure.services.s3_file_storage import S3Config, S3FileStorageService


@pytest.fixture
def s3_service() -> S3FileStorageService:
    config = S3Config(
        bucket="test-bucket",
        region="us-east-1",
        endpoint_url="http://localhost:9000",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    return S3FileStorageService(config)


@pytest.fixture
def mock_s3_client() -> MagicMock:
    client = MagicMock()
    client.put_object = AsyncMock(return_value={"ETag": '"test-etag"'})
    client.get_object = AsyncMock(
        return_value={"Body": AsyncMock(read=AsyncMock(return_value=b"file-content"))}
    )
    client.delete_object = AsyncMock(return_value={})
    client.generate_presigned_url = AsyncMock(return_value="https://presigned.url")
    return client


@pytest.mark.asyncio
class TestS3FileStorageService:
    async def test_upload_returns_etag(self, s3_service, mock_s3_client) -> None:
        with patch.object(s3_service, "_session") as mock_session:
            mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

            key = ObjectKey("books/1/file.epub")
            etag = await s3_service.upload(
                key=key,
                content=b"data",
                content_type="application/epub+zip",
                storage_class=StorageClass("STANDARD"),
            )

            mock_s3_client.put_object.assert_awaited_once_with(
                Bucket="test-bucket",
                Key="books/1/file.epub",
                Body=b"data",
                ContentType="application/epub+zip",
                StorageClass="STANDARD",
            )
            assert isinstance(etag, Etag)
            assert etag._name == "test-etag"

    async def test_download_returns_bytes(self, s3_service, mock_s3_client) -> None:
        with patch.object(s3_service, "_session") as mock_session:
            mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

            content = await s3_service.download(ObjectKey("books/1/file.epub"))

            mock_s3_client.get_object.assert_awaited_once_with(
                Bucket="test-bucket",
                Key="books/1/file.epub",
            )
            assert content == b"file-content"

    async def test_delete(self, s3_service, mock_s3_client) -> None:
        with patch.object(s3_service, "_session") as mock_session:
            mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

            await s3_service.delete(ObjectKey("books/1/file.epub"))

            mock_s3_client.delete_object.assert_awaited_once_with(
                Bucket="test-bucket",
                Key="books/1/file.epub",
            )

    async def test_get_presigned_url(self, s3_service, mock_s3_client) -> None:
        with patch.object(s3_service, "_session") as mock_session:
            mock_session.return_value.client.return_value.__aenter__.return_value = mock_s3_client

            url = await s3_service.get_presigned_url(ObjectKey("books/1/file.epub"), expires_in=120)

            mock_s3_client.generate_presigned_url.assert_awaited_once_with(
                "get_object",
                Params={"Bucket": "test-bucket", "Key": "books/1/file.epub"},
                ExpiresIn=120,
            )
            assert url == "https://presigned.url"