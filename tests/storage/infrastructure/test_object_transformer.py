from src.storage.domain.value_objects.etag import Etag
from src.storage.domain.value_objects.object_key import ObjectKey
from src.storage.domain.value_objects.storage_class import StorageClass
from src.storage.infrastructure.sql.models.object_model import ObjectModel
from src.storage.infrastructure.sql.transformers.object_transformer import ObjectTransformer

from tests.storage.infrastructure.factories import make_object


class TestObjectTransformerToModel:
    def test_converts_entity_to_model(self) -> None:
        entity = make_object(
            key="books/1/file.epub",
            content_type="application/epub+zip",
            storage_class="GLACIER",
            size=2048,
            etag="deadbeef",
        )

        model = ObjectTransformer.to_model(entity)

        assert model.key == "books/1/file.epub"
        assert model.content_type == "application/epub+zip"
        assert model.storage_class == "GLACIER"
        assert model.size == 2048
        assert model.etag == "deadbeef"
        assert model.is_deleted is False


class TestObjectTransformerToDomain:
    def test_converts_model_to_entity(self) -> None:
        model = ObjectModel(
            key="books/2/file.pdf",
            content_type="application/pdf",
            storage_class="STANDARD_IA",
            size=4096,
            etag="cafebabe",
            is_deleted=False,
        )

        entity = ObjectTransformer.to_domain(model)

        assert isinstance(entity.key, ObjectKey)
        assert entity.key._value == "books/2/file.pdf"
        assert entity.content_type == "application/pdf"
        assert isinstance(entity.storage_class, StorageClass)
        assert entity.storage_class.name == "STANDARD_IA"
        assert entity.size == 4096
        assert isinstance(entity.etag, Etag)
        assert entity.etag._name == "cafebabe"
        assert entity.is_deleted is False