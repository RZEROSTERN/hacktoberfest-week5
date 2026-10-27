import json
import time
from collections import Counter
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.canon_validation import validate_proposal
from app.ollama import Proposal, capture_stream, local_origin
from app.story import load_story

ROOT = Path(__file__).resolve().parents[2]


def test_stream_capture_distinguishes_first_fragment_from_completion() -> None:
    lines = [
        json.dumps({"message": {"content": '{"relevant":true,'}, "done": False}),
        json.dumps({"message": {"content": '"reply":"Aquí estoy.","fact_ids":[]}'}}),
        json.dumps({"done": True, "done_reason": "stop", "eval_count": 18}),
    ]
    captured = capture_stream(lines, time.perf_counter(), 2)
    assert captured.first_token_s is not None
    assert captured.full_s >= captured.first_token_s
    assert Proposal.model_validate_json(captured.raw).reply == "Aquí estoy."
    assert captured.metrics["eval_count"] == 18


def test_incomplete_and_error_streams_are_not_accepted() -> None:
    with pytest.raises(ValueError, match="Incomplete"):
        capture_stream([json.dumps({"message": {"content": "{"}})], time.perf_counter(), 1)
    with pytest.raises(ValueError, match="generation error"):
        capture_stream([json.dumps({"error": "stopped"})], time.perf_counter(), 1)


def test_invalid_schema_does_not_become_a_valid_classification() -> None:
    with pytest.raises(ValidationError):
        Proposal.model_validate({"relevant": "true", "reply": "Hello.", "fact_ids": []})
    with pytest.raises(ValidationError):
        Proposal(relevant=True, reply="", fact_ids=[])


@pytest.mark.parametrize(
    "origin",
    [
        "https://ollama.com",
        "http://127.0.0.1@evil.example:1234",
        "http://0.0.0.0:1234",
        "http://127.0.0.1:1234/path",
        "http://127.0.0.1:1234?redirect=elsewhere",
    ],
)
def test_transport_refuses_non_loopback_origins(origin: str) -> None:
    with pytest.raises(ValueError):
        local_origin(origin)


def test_validator_catches_locked_facts_and_swapped_known_relationships() -> None:
    story = load_story(ROOT / "content")
    locked = Proposal(relevant=True, reply="My father Aurelio taught me.", fact_ids=["trade"])
    assert "unavailable_fact_reference" in validate_proposal(story, locked, set())
    swapped = Proposal(relevant=False, reply="My father Ernesto taught me.", fact_ids=[])
    assert "wrong_relationship" in validate_proposal(
        story, swapped, {obj.id for obj in story.objects}
    )


def test_authored_recovered_lines_survive_the_prototype_validator() -> None:
    story = load_story(ROOT / "content")
    for obj in story.objects:
        for text in [obj.fallbacks.recovered.en, obj.fallbacks.recovered.es]:
            proposed = Proposal(relevant=True, reply=text, fact_ids=[])
            assert validate_proposal(story, proposed, {item.id for item in story.objects}) == []


def test_benchmark_corpus_is_balanced_and_complete() -> None:
    cases = json.loads((ROOT / "spike/cases.json").read_text())
    assert len(cases) == 120
    assert len({case["id"] for case in cases}) == 120
    for obj in load_story(ROOT / "content").objects:
        selected = [case for case in cases if case["object_id"] == obj.id]
        assert Counter(case["language"] for case in selected) == {"en": 10, "es": 10}
        assert Counter(case["kind"] for case in selected) == {
            "relevant": 8,
            "irrelevant": 6,
            "adversarial": 6,
        }
