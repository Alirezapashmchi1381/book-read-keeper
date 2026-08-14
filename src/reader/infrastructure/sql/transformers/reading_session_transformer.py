from src.reader.domain.entities.reading_session import ReadingSession
from src.reader.domain.value_objects.device_id import DeviceId
from src.reader.domain.value_objects.locator import Locator
from src.reader.domain.value_objects.progress_percent import ProgressPercent
from src.reader.infrastructure.sql.models.reading_session_model import ReadingSessionModel


class ReadingSessionTransformer:
    @staticmethod
    def to_domain(model: ReadingSessionModel) -> ReadingSession:
        return ReadingSession(
            id=model.id,
            user_id=model.user_id,
            book_id=model.book_id,
            locator=Locator(
                book_id=model.book_id,
                value=model.locator_value,
                provider=model.locator_provider,
                sort_key=model.locator_sort_key,
                chapter_number=model.locator_chapter_number,
                chapter_title=model.locator_chapter_title,
            ),
            progress_percent=ProgressPercent(model.progress_percent),
            device_id=DeviceId(model.device_id) if model.device_id else None,
            started_at=model.started_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: ReadingSession) -> ReadingSessionModel:
        return ReadingSessionModel(
            id=entity.id,
            user_id=entity.user_id,
            book_id=entity.book_id,
            locator_value=entity.locator.value,
            locator_provider=entity.locator.provider,
            locator_sort_key=entity.locator.sort_key,
            locator_chapter_number=entity.locator.chapter_number,
            locator_chapter_title=entity.locator.chapter_title,
            progress_percent=entity.progress_percent.value,
            device_id=entity.device_id.value if entity.device_id else None,
            started_at=entity.started_at,
            updated_at=entity.updated_at,
        )