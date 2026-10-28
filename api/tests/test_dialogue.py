import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from app import dialogue
from app.dialogue import interpret, reply_choices, resolve_choice
from app.ollama import Capture
from app.story import load_story

ROOT = Path(__file__).resolve().parents[2]
STORY = load_story(ROOT / "content")


def test_reply_ids_are_scoped_to_object_recovery_relevance_and_language() -> None:
    for obj in STORY.objects:
        for language in ("en", "es"):
            for recovered in (set(), {obj.id}, {x.id for x in STORY.objects if x.id != obj.id}):
                for relevant in (False, True):
                    choices = reply_choices(STORY, obj.id, recovered, relevant, language)
                    if not relevant:
                        expected = {f"{obj.id}.unrelated", f"{obj.id}.redirect"}
                    elif obj.id in recovered:
                        expected = {f"{obj.id}.recovered", "shared.memory_recovered"}
                    else:
                        expected = {f"{obj.id}.unrecovered", f"{obj.id}.connected"}
                    assert set(choices) == expected
                    for key, text in choices.items():
                        assert resolve_choice(json.dumps({"reply_id": key}), choices) == (key, text)
                    for other in STORY.objects:
                        if other.id != obj.id:
                            with pytest.raises(ValueError):
                                resolve_choice(
                                    json.dumps({"reply_id": f"{other.id}.recovered"}), choices
                                )


@pytest.mark.parametrize(
    "raw",
    [
        '{"reply_id":"photograph.recovered"}',
        '{"reply_id":"shared.memory_recovered"}',
        '{"reply_id":"photograph.connected", "reply":"My name is Maria."}',
        '{"reply_id":"photograph.connected"} My name is Maria.',
        'My name is Maria. {"reply_id":"photograph.connected"}',
        '```json\n{"reply_id":"photograph.connected"}\n```',
        '{"reply_id":["photograph.connected"]}',
        '{"reply_id":null}',
        '{"reply_id":"photograph.connected radio.recovered"}',
    ],
)
def test_whole_response_rejects_prose_extra_fields_and_locked_memories(raw: str) -> None:
    with pytest.raises(ValueError):
        resolve_choice(raw, reply_choices(STORY, "photograph", set(), True, "en"))


def call_interpreter() -> dialogue.Dialogue:
    return interpret(
        STORY,
        "photograph",
        set(),
        "en",
        "Could that be your family?",
        origin="http://127.0.0.1:12345",
        model="local-test",
        prompts=ROOT / "api/prompts",
        think=None,
    )


def test_bad_choice_is_regenerated_once_and_only_authored_text_is_exposed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    outputs = iter(
        [
            '{"relevant":true}',
            '{"reply_id":"photograph.connected","reply":"I am Maria."}',
            '{"reply_id":"photograph.connected"}',
        ]
    )

    def scripted(*args: Any, **kwargs: Any) -> Capture:
        return Capture(raw=next(outputs), done=True)

    monkeypatch.setattr(dialogue, "chat", scripted)
    result = call_interpreter()
    assert result.relevant is True
    assert len(result.attempts) == 2
    assert not result.fallback_used
    assert result.reply == STORY.objects[0].fallbacks.connected.en
    assert "Maria" not in result.reply


def test_failed_classifier_does_not_unlock_or_call_the_selector(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unavailable(*args: Any, **kwargs: Any) -> Capture:
        raise httpx.ConnectError("Local engine unavailable")

    monkeypatch.setattr(dialogue, "chat", unavailable)
    result = call_interpreter()
    assert result.relevant is None
    assert result.attempts == []
    assert result.fallback_used
    assert result.reply == STORY.objects[0].fallbacks.error.en


def test_two_invalid_choices_use_authored_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    outputs = iter(
        [
            '{"relevant":false}',
            '{"reply_id":"photograph.recovered"}',
            '{"reply_id":"photograph.recovered"}',
        ]
    )

    def scripted(*args: Any, **kwargs: Any) -> Capture:
        return Capture(raw=next(outputs), done=True)

    monkeypatch.setattr(dialogue, "chat", scripted)
    result = call_interpreter()
    assert result.relevant is False
    assert len(result.attempts) == 2
    assert result.fallback_used
    assert result.reply == STORY.objects[0].fallbacks.error.en


def test_holdout_has_fixed_balanced_labels_and_new_messages() -> None:
    rows = json.loads((ROOT / "spike/holdout.json").read_text())
    original = json.loads((ROOT / "spike/cases.json").read_text())
    assert len(rows) == 120
    assert len({r["id"] for r in rows}) == 120
    assert not {r["message"] for r in rows} & {r["message"] for r in original}
    for obj in STORY.objects:
        selected = [r for r in rows if r["object_id"] == obj.id]
        assert sum(r["expected_relevant"] for r in selected) == 8
        assert sum(r["kind"] == "adversarial" for r in selected) == 6
        assert sum(r["language"] == "en" for r in selected) == 10
