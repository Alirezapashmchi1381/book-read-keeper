from src.annotations.domain.entities.highlight import Highlight
from src.annotations.domain.value_objects.chapter import Chapter
from src.annotations.domain.value_objects.locator import Locator
from src.annotations.domain.value_objects.note_text import NoteText
from src.annotations.infrastructure.sql.models.highlight_model import HighlightModel


class HighlightTransformer:
    @staticmethod
    def _build_chapter(number: int | None, title: str | None) -> Chapter | None:
        if number is None:
            return None
        return Chapter(number=number, title=title)

    @staticmethod
    def _build_locator(
        *,
        book_id,
        value,
        provider,
        sort_key,
        chapter_number,
        chapter_title,
    ) -> Locator:
        return Locator(
            book_id=book_id,
            value=value,
            provider=provider,
            sort_key=sort_key,
            chapter=HighlightTransformer._build_chapter(chapter_number, chapter_title),
        )

    @staticmethod
    def to_domain(model: HighlightModel) -> Highlight:
        return Highlight(
            id=model.id,
            user_id=model.user_id,
            locator=HighlightTransformer._build_locator(
                book_id=model.book_id,
                value=model.start_value,
                provider=model.start_provider,
                sort_key=model.start_sort_key,
                chapter_number=model.start_chapter_number,
                chapter_title=model.start_chapter_title,
            ),
            end_locator=HighlightTransformer._build_locator(
                book_id=model.book_id,
                value=model.end_value,
                provider=model.end_provider,
                sort_key=model.end_sort_key,
                chapter_number=model.end_chapter_number,
                chapter_title=model.end_chapter_title,
            ),
            selected_text=model.selected_text,
            color=model.color,
            note=NoteText(model.note) if model.note else None,
            is_deleted=model.is_deleted,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Highlight) -> HighlightModel:
        start = entity.locator
        end = entity.end_locator
        return HighlightModel(
            id=entity.id,
            user_id=entity.user_id,
            book_id=start.book_id,
            selected_text=entity.selected_text,
            color=entity.color,
            note=entity.note.value if entity.note else None,
            start_value=start.value,
            start_provider=start.provider,
            start_sort_key=start.sort_key,
            start_chapter_number=start.chapter.number if start.chapter else None,
            start_chapter_title=start.chapter.title if start.chapter else None,
            end_value=end.value,
            end_provider=end.provider,
            end_sort_key=end.sort_key,
            end_chapter_number=end.chapter.number if end.chapter else None,
            end_chapter_title=end.chapter.title if end.chapter else None,
            is_deleted=entity.is_deleted,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )