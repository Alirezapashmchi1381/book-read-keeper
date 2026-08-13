from uuid import uuid4

from src.annotations.domain.entities.highlight import Highlight
from src.annotations.domain.value_objects.locator import Locator
from src.annotations.domain.value_objects.note_text import NoteText
from src.annotations.infrastructure.sql.models.highlight_model import HighlightModel
from src.annotations.infrastructure.sql.transformers.highlight_transformer import HighlightTransformer

from tests.annotations.infrastructure.factories import make_highlight


class TestHighlightTransformer:
    def test_to_model_flattens_entity(self) -> None:
        entity: Highlight = make_highlight(selected_text="text", note="a note")

        model = HighlightTransformer.to_model(entity)

        assert model.id == entity.id
        assert model.user_id == entity.user_id
        assert model.book_id == entity.locator.book_id
        assert model.selected_text == "text"
        assert model.color == entity.color
        assert model.note == "a note"
        assert model.start_value == entity.locator.value
        assert model.start_provider == entity.locator.provider
        assert model.start_sort_key == entity.locator.sort_key
        assert model.start_chapter_number == 1
        assert model.end_value == entity.end_locator.value
        assert model.end_sort_key == entity.end_locator.sort_key

    def test_to_domain_rebuilds_entity(self) -> None:
        model = HighlightModel(
            id=uuid4(),
            user_id=uuid4(),
            book_id=uuid4(),
            selected_text="text",
            color="#FF5733",
            note="a note",
            start_value="cfi-1",
            start_provider="epub",
            start_sort_key="1.0",
            start_chapter_number=1,
            start_chapter_title="Chapter 1",
            end_value="cfi-2",
            end_provider="epub",
            end_sort_key="1.1",
            end_chapter_number=1,
            end_chapter_title="Chapter 1",
            is_deleted=False,
        )

        entity = HighlightTransformer.to_domain(model)

        assert isinstance(entity, Highlight)
        assert entity.id == model.id
        assert entity.selected_text == "text"
        assert isinstance(entity.note, NoteText)
        assert entity.note.value == "a note"
        assert isinstance(entity.locator, Locator)
        assert entity.locator.value == "cfi-1"
        assert entity.locator.chapter is not None
        assert entity.locator.chapter.number == 1
        assert entity.end_locator.value == "cfi-2"
        assert entity.end_locator.chapter.title == "Chapter 1"