from uuid import uuid4

from src.reader.domain.entities.reading_session import ReadingSession
from src.reader.domain.value_objects.locator import Locator
from src.reader.domain.value_objects.progress_percent import ProgressPercent
from src.reader.infrastructure.sql.models.reading_session_model import ReadingSessionModel
from src.reader.infrastructure.sql.transformers.reading_session_transformer import ReadingSessionTransformer

from tests.reader.infrastructure.factories import make_session


class TestReadingSessionTransformer:
    def test_to_model_flattens_entity(self) -> None:
        entity = make_session(progress=42.5, device_id="device-1")

        model = ReadingSessionTransformer.to_model(entity)

        assert model.id == entity.id
        assert model.user_id == entity.user_id
        assert model.book_id == entity.book_id
        assert model.locator_value == entity.locator.value
        assert model.locator_provider == entity.locator.provider
        assert model.locator_sort_key == entity.locator.sort_key
        assert model.locator_chapter_number == 1
        assert model.progress_percent == 42.5
        assert model.device_id == "device-1"

    def test_to_domain_rebuilds_entity(self) -> None:
        model = ReadingSessionModel(
            id=uuid4(),
            user_id=uuid4(),
            book_id=uuid4(),
            locator_value="cfi-1",
            locator_provider="epub",
            locator_sort_key="1.0",
            locator_chapter_number=1,
            locator_chapter_title="Chapter 1",
            progress_percent=50.0,
            device_id="device-1",
        )

        entity = ReadingSessionTransformer.to_domain(model)

        assert isinstance(entity, ReadingSession)
        assert entity.id == model.id
        assert entity.progress_percent.value == 50.0
        assert isinstance(entity.locator, Locator)
        assert entity.locator.value == "cfi-1"
        assert entity.locator.chapter_number == 1
        assert entity.device_id is not None
        assert entity.device_id.value == "device-1"