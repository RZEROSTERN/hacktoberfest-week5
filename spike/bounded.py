"""Benchmark the exact authored-reply interpreter intended for the game."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

from app.dialogue import interpret, reply_choices, resolve_choice
from app.story import Story

ROOT = Path(__file__).resolve().parents[1]
Json = dict[str, Any]


class Meter(Protocol):
    case_peak: int
    case_footprint: int


def boundary_report(story: Story, fixtures: list[Json]) -> Json:
    """Replay recorded false prose beside valid IDs across live legal choices.

    These check output confinement, not the classifier's semantic accuracy.
    Approved content itself was reviewed separately in the story step.
    """
    caught = total = controls = false_rejections = 0
    failures = []
    for obj in story.objects:
        for language in ("en", "es"):
            for recovered in (set(), {obj.id}):
                for relevant in (False, True):
                    choices = reply_choices(
                        story, obj.id, recovered, relevant, language
                    )
                    for reply_id in choices:
                        controls += 1
                        try:
                            resolve_choice(json.dumps({"reply_id": reply_id}), choices)
                        except ValueError:
                            false_rejections += 1
                    for fixture in fixtures:
                        if fixture["allowed"] or fixture["language"] != language:
                            continue
                        total += 1
                        raw = json.dumps(
                            {"reply_id": next(iter(choices)), "reply": fixture["reply"]}
                        )
                        try:
                            resolve_choice(raw, choices)
                            failures.append(
                                {"object_id": obj.id, "fixture": fixture["id"]}
                            )
                        except ValueError:
                            caught += 1
    return {
        "method": "whole JSON and authored ID confinement; injected extra prose",
        "contradictions": total,
        "caught": caught,
        "good_controls": controls,
        "false_rejections": false_rejections,
        "failures": failures,
    }


def run_case(
    origin: str, model: str, case: Json, story: Story, memory: Meter, config: Json
) -> Json:
    memory.case_peak = 0
    memory.case_footprint = 0
    result = interpret(
        story,
        case["object_id"],
        set(case["recovered"]),
        case["language"],
        case["message"],
        origin=origin,
        model=model,
        prompts=ROOT / "api/prompts",
        think=config["think"],
        timeout_s=config["timeout_s"],
        num_ctx=config["num_ctx"],
    )
    attempts = [
        {
            **(
                {
                    "raw": a.capture.raw,
                    "first_token_s": a.capture.first_token_s,
                    "full_s": a.capture.full_s,
                    "metrics": a.capture.metrics,
                }
                if a.capture
                else {}
            ),
            "reasons": [a.error] if a.error else [],
        }
        for a in result.attempts
    ]
    first = result.attempts[0].capture if result.attempts else None
    classification = result.classification
    choices = (
        reply_choices(
            story,
            case["object_id"],
            set(case["recovered"]),
            result.relevant,
            case["language"],
        )
        if result.relevant is not None
        else {}
    )
    return {
        **case,
        "predicted_relevant": result.relevant,
        "classification_correct": result.relevant is case["expected_relevant"],
        "classification": {
            "raw": classification.raw if classification else None,
            "metrics": classification.metrics if classification else {},
            "full_s": result.classification_s,
            "error": result.classification_error,
        },
        "attempts": attempts,
        "allowed_reply_ids": list(choices),
        "fallback_used": result.fallback_used,
        "safe_reply": result.reply,
        "safe_reply_id": result.reply_id,
        "safe_reply_source": "authored",
        "raw_first_token_s": result.classification_s + first.first_token_s
        if first and first.first_token_s is not None
        else None,
        "raw_full_reply_s": result.classification_s + first.full_s if first else None,
        "validated_first_token_s": result.pipeline_s,
        "pipeline_s": result.pipeline_s,
        "peak_tree_rss_bytes": memory.case_peak,
        "peak_tree_physical_footprint_bytes": memory.case_footprint,
    }
