"""Local-only streaming capture used by the model spike; no runtime model default."""

import json
import time
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel, ConfigDict, Field


class Proposal(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    relevant: bool
    reply: str = Field(min_length=1, max_length=600)
    fact_ids: list[str]


class Classification(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    relevant: bool


def thinking_control(metadata: dict[str, Any]) -> bool | None:
    """Disable supported thinking; omit the control on a non-thinking model."""
    values = metadata.get("thinking", {}).get("values", [])
    if False in values or "thinking" in metadata.get("capabilities", []):
        return False
    return None


def proposal_schema(visible_ids: list[str]) -> dict[str, object]:
    schema = Proposal.model_json_schema()
    items: dict[str, object] = {"type": "string"}
    if visible_ids:
        items["enum"] = sorted(visible_ids)
    schema["properties"]["fact_ids"] = {
        "type": "array",
        "items": items,
        "maxItems": len(visible_ids),
        "uniqueItems": True,
    }
    return schema


@dataclass
class Capture:
    raw: str = ""
    first_token_s: float | None = None
    full_s: float = 0
    done: bool = False
    metrics: dict[str, int | str] = field(default_factory=dict)


def capture_stream(lines: Iterable[str], started: float, timeout_s: float) -> Capture:
    """Capture raw transport timing; this does not authorize showing any tokens."""
    result = Capture()
    for line in lines:
        elapsed = time.perf_counter() - started
        if elapsed > timeout_s:
            raise TimeoutError("Local generation exceeded its wall-clock deadline")
        if not line.strip():
            continue
        item = json.loads(line)
        if item.get("error"):
            raise ValueError("Ollama reported a generation error")
        fragment = item.get("message", {}).get("content", "")
        if fragment:
            if result.first_token_s is None:
                result.first_token_s = elapsed
            result.raw += fragment
        if item.get("done"):
            result.done = True
            result.metrics = {
                key: item[key]
                for key in (
                    "done_reason",
                    "load_duration",
                    "prompt_eval_count",
                    "prompt_eval_duration",
                    "eval_count",
                    "eval_duration",
                    "total_duration",
                )
                if key in item
            }
            break
    result.full_s = time.perf_counter() - started
    if not result.done:
        raise ValueError("Incomplete Ollama stream")
    return result


def local_origin(value: str) -> str:
    parsed = urlparse(value)
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or parsed.username
        or parsed.password
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
        or parsed.port is None
    ):
        raise ValueError("A private loopback origin is required")
    return value.rstrip("/")


def chat(
    origin: str,
    model: str,
    messages: list[dict[str, str]],
    *,
    visible_fact_ids: list[str],
    timeout_s: float = 60,
    num_ctx: int = 4096,
    num_predict: int = 128,
    think: bool | None = False,
    schema: dict[str, object] | None = None,
    keep_alive: str | int = "30s",
) -> Capture:
    if "cloud" in model.casefold():
        raise ValueError("Cloud model names are not permitted")
    body = {
        "model": model,
        "messages": messages,
        "stream": True,
        "format": schema if schema is not None else proposal_schema(visible_fact_ids),
        "keep_alive": keep_alive,
        "options": {"temperature": 0, "seed": 42, "num_ctx": num_ctx, "num_predict": num_predict},
    }
    if think is not None:
        body["think"] = think
    # Ignore proxy environment variables: prompts must never reach an external proxy.
    with httpx.Client(base_url=local_origin(origin), timeout=timeout_s, trust_env=False) as client:
        started = time.perf_counter()
        with client.stream("POST", "/api/chat", json=body) as response:
            response.raise_for_status()
            return capture_stream(response.iter_lines(), started, timeout_s)
