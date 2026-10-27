import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.story import Story, load_story

CONTENT = Path(__file__).resolve().parents[2] / "content"


def test_authored_story_is_complete_in_both_languages() -> None:
    story = load_story(CONTENT)
    assert len(story.objects) == 6
    assert story.canon.spirit.name == "Inés Robles Vega"
    assert story.canon.spirit.died.year - story.canon.spirit.born.year == 76
    assert {ending.condition for ending in story.endings} == {
        "all_memories",
        "some_memories",
        "no_memories",
    }


@pytest.mark.parametrize("language", ["en", "es"])
def test_missing_translation_is_refused(language: str) -> None:
    data = load_story(CONTENT).model_dump(mode="json")
    del data["objects"][0]["memory"]["scene"][language]
    with pytest.raises(ValidationError):
        Story.model_validate(data)


def test_invalid_reveal_and_fact_references_are_refused() -> None:
    data = load_story(CONTENT).model_dump(mode="json")
    data["objects"][0]["memory"]["fact_ids"].append("invented-fact")
    with pytest.raises(ValidationError, match="Unknown fact"):
        Story.model_validate(data)

    data = load_story(CONTENT).model_dump(mode="json")
    data["canon"]["facts"][0]["revealed_by"] = ["invented-object"]
    with pytest.raises(ValidationError, match="Unknown reveal"):
        Story.model_validate(data)


def test_missing_fallback_and_duplicate_objects_are_refused() -> None:
    data = load_story(CONTENT).model_dump(mode="json")
    del data["objects"][0]["fallbacks"]["error"]
    with pytest.raises(ValidationError):
        Story.model_validate(data)

    data = load_story(CONTENT).model_dump(mode="json")
    data["objects"][1]["id"] = data["objects"][0]["id"]
    with pytest.raises(ValidationError, match="Duplicate object"):
        Story.model_validate(data)


def test_missing_ending_category_is_refused() -> None:
    data = load_story(CONTENT).model_dump(mode="json")
    data["endings"][0]["condition"] = "no_memories"
    with pytest.raises(ValidationError, match="three ending conditions"):
        Story.model_validate(data)


def test_content_can_be_loaded_from_a_packaged_style_directory(tmp_path: Path) -> None:
    destination = tmp_path / "vela-á" / "content"
    destination.mkdir(parents=True)
    for source in CONTENT.glob("*.json"):
        destination.joinpath(source.name).write_text(source.read_text(), encoding="utf-8")
    assert load_story(destination).canon.id == load_story(CONTENT).canon.id
    # Human review status is explicit data, never inferred from passing structural checks.
    assert json.loads((CONTENT / "canon.json").read_text())["review_status"] in {
        "pending_owner_approval",
        "approved",
    }
