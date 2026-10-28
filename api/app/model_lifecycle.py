"""Prepare a consented, installed local model before accepting player messages."""

import time
from dataclasses import dataclass
from typing import Any

import httpx

from app.ollama import local_origin, thinking_control


@dataclass(frozen=True)
class PreparedModel:
    model: str
    startup_s: float
    think: bool | None
    loaded: dict[str, Any]
    metrics: dict[str, Any]


def prepare_model(
    origin: str, model: str, *, timeout_s: float = 60, num_ctx: int = 4096
) -> PreparedModel:
    """Load existing weights, verify residency, and keep them until explicit cleanup.

    There is no pull/download path. Callers show preparation progress and gate
    dialogue until this succeeds, or explicitly enter authored fallback mode.
    The desktop owns this engine; its shutdown always stops the entire tree.
    """
    if "cloud" in model.casefold():
        raise ValueError("Cloud models are not permitted")
    started = time.perf_counter()
    with httpx.Client(base_url=local_origin(origin), timeout=timeout_s, trust_env=False) as client:
        shown = client.post("/api/show", json={"model": model})
        shown.raise_for_status()
        metadata = shown.json()
        if metadata.get("remote_host"):
            raise ValueError("Remote models are not permitted")
        response = client.post(
            "/api/generate",
            json={
                "model": model,
                "stream": False,
                "keep_alive": -1,
                "options": {"num_ctx": num_ctx},
            },
        )
        response.raise_for_status()
        metrics = response.json()
        if metrics.get("error") or not metrics.get("done"):
            raise ValueError("Local model preparation did not complete")
        status = client.get("/api/ps")
        status.raise_for_status()
        loaded = next(
            (
                item
                for item in status.json().get("models", [])
                if item.get("name") == model or item.get("model") == model
            ),
            None,
        )
        if loaded is None:
            raise ValueError("Prepared model is not resident")
    return PreparedModel(
        model=model,
        startup_s=time.perf_counter() - started,
        think=thinking_control(metadata),
        loaded=loaded,
        metrics=metrics,
    )
