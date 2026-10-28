"""Local semantic interpretation with authored, state-scoped dialogue selection."""

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict

from app.ollama import Capture, Classification, chat
from app.story import Story

Language = Literal["en", "es"]


class ReplyChoice(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    reply_id: str


def reply_choices(
    story: Story, object_id: str, recovered: set[str], relevant: bool, language: Language
) -> dict[str, str]:
    """Build the complete allowed surface from authored content, before inference."""
    obj = next((item for item in story.objects if item.id == object_id), None)
    if obj is None or not recovered <= {item.id for item in story.objects}:
        raise ValueError("Unknown object or recovery state")
    if not relevant:
        states = ("unrelated", "redirect")
    elif object_id in recovered:
        return {
            f"{object_id}.recovered": getattr(obj.fallbacks.recovered, language),
            "shared.memory_recovered": getattr(story.lines["memory_recovered"], language),
        }
    else:
        states = ("unrecovered", "connected")
    return {
        f"{object_id}.{state}": getattr(getattr(obj.fallbacks, state), language) for state in states
    }


def choice_schema(choices: dict[str, str]) -> dict[str, object]:
    schema = ReplyChoice.model_json_schema()
    schema["properties"]["reply_id"]["enum"] = list(choices)
    return schema


def resolve_choice(raw: str, choices: dict[str, str]) -> tuple[str, str]:
    """Strict whole-response parsing; never extract or display generated prose."""
    choice = ReplyChoice.model_validate_json(raw)
    if choice.reply_id not in choices:
        raise ValueError("reply_id is unavailable for this object and state")
    return choice.reply_id, choices[choice.reply_id]


@dataclass
class Attempt:
    capture: Capture | None = None
    error: str | None = None


@dataclass
class Dialogue:
    relevant: bool | None
    reply: str
    reply_id: str
    fallback_used: bool = True
    classification: Capture | None = None
    classification_error: str | None = None
    classification_s: float = 0
    pipeline_s: float = 0
    attempts: list[Attempt] = field(default_factory=list)


def interpret(
    story: Story,
    object_id: str,
    recovered: set[str],
    language: Language,
    message: str,
    *,
    origin: str,
    model: str,
    prompts: Path,
    think: bool | None,
    timeout_s: float = 6,
    num_ctx: int = 4096,
) -> Dialogue:
    """One classifier, then one selector with at most one regeneration.

    Callers serialize interactions and own clock/memory progression. Raw captures
    are in-memory benchmark evidence, never a player-facing response or log.
    """
    reply_choices(story, object_id, recovered, False, language)
    obj = next(item for item in story.objects if item.id == object_id)
    fallback = "recovered" if object_id in recovered else "error"
    result = Dialogue(
        relevant=None,
        reply=getattr(getattr(obj.fallbacks, fallback), language),
        reply_id=f"{object_id}.{fallback}",
    )
    started = time.perf_counter()

    def remaining() -> float:
        budget = timeout_s - (time.perf_counter() - started)
        if budget <= 0:
            raise TimeoutError("Dialogue deadline exceeded")
        return budget

    classifier = (prompts / "relevance.spike.v3.txt").read_text(encoding="utf-8")
    context = {
        "object": getattr(obj.title, language),
        "description": getattr(obj.description, language),
        "relevant_topics": getattr(obj.relevance.accept, language),
        "player_message": message,
    }
    try:
        result.classification = chat(
            origin,
            model,
            [
                {"role": "system", "content": classifier},
                {"role": "user", "content": json.dumps(context, ensure_ascii=False)},
            ],
            visible_fact_ids=[],
            timeout_s=remaining(),
            num_ctx=num_ctx,
            num_predict=32,
            think=think,
            schema=Classification.model_json_schema(),
        )
        result.relevant = Classification.model_validate_json(result.classification.raw).relevant
    except (httpx.HTTPError, ValueError, TimeoutError) as error:
        result.classification_error = type(error).__name__
        result.pipeline_s = time.perf_counter() - started
        result.classification_s = result.pipeline_s
        return result
    result.classification_s = time.perf_counter() - started
    choices = reply_choices(story, object_id, recovered, result.relevant, language)
    schema = choice_schema(choices)
    selector = (prompts / "reply-selection.v1.txt").read_text(encoding="utf-8")
    messages = [
        {"role": "system", "content": selector},
        {
            "role": "user",
            "content": json.dumps(
                {
                    "relevant": result.relevant,
                    "choices": choices,
                    "player_message": message,
                    "schema": schema,
                },
                ensure_ascii=False,
            ),
        },
    ]
    for index in range(2):
        attempt = Attempt()
        result.attempts.append(attempt)
        try:
            attempt.capture = chat(
                origin,
                model,
                messages,
                visible_fact_ids=[],
                timeout_s=remaining(),
                num_ctx=num_ctx,
                num_predict=48,
                think=think,
                schema=schema,
            )
            result.reply_id, result.reply = resolve_choice(attempt.capture.raw, choices)
            result.fallback_used = False
            break
        except (httpx.HTTPError, ValueError, TimeoutError) as error:
            attempt.error = type(error).__name__
            if attempt.capture is None:
                break
            if index == 0:
                messages.extend(
                    [
                        {"role": "assistant", "content": attempt.capture.raw},
                        {
                            "role": "user",
                            "content": "Invalid response. Return only one reply_id from choices, "
                            "with no extra fields or text.",
                        },
                    ]
                )
    result.pipeline_s = time.perf_counter() - started
    return result
