"""Loopback API for validated, authored dialogue and model readiness."""

import contextlib
import json
import sys
from pathlib import Path
from threading import Lock
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from app.config import Settings
from app.dialogue import interpret
from app.model_lifecycle import PreparedModel, prepare_model
from app.setup import SetupManager
from app.story import Story, load_story


class Health(BaseModel):
    status: str = "ok"


class Readiness(BaseModel):
    mode: Literal["ready", "fallback"]


class SetupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    model: str = Field(min_length=1, max_length=200)
    consent: Literal[True]


class ModelInfo(BaseModel):
    tag: str
    name: str
    license: str
    source: str
    tested_digest: str
    download_bytes: int
    context_tokens: int
    thinking: bool
    requires_preparation: bool
    benchmark: str


class SetupStatus(BaseModel):
    setup_complete: bool
    selected_model: str | None
    state: Literal["idle", "downloading", "checking", "ready", "failed"]
    completed: int
    total: int
    error: str | None
    models: list[ModelInfo]
    memory_available: int
    disk_available: int | None


class DialogueRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    object_id: str
    recovered: list[str] = Field(max_length=6)
    language: Literal["en", "es"]
    message: str = Field(min_length=1, max_length=1000)


class DialogueResponse(BaseModel):
    relevant: bool | None
    reply: str
    fallback_used: bool


def resource_root() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))


def selected_model(directory: Path) -> str | None:
    """Read player-owned settings; absence never triggers a download."""
    try:
        settings = json.loads((directory / "settings.json").read_text(encoding="utf-8"))
        model = settings.get("model")
        if isinstance(model, str) and 0 < len(model) <= 200 and "cloud" not in model.casefold():
            return model
    except (OSError, ValueError, AttributeError):
        pass
    return None


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="The Last Candle local API", version="1.0.0")
    app.state.settings = settings
    app.state.prepared = None
    app.state.inference_lock = Lock()
    root = resource_root()
    prompts = root / "prompts" if getattr(sys, "frozen", False) else root / "api" / "prompts"
    app.state.setup = SetupManager(
        settings.data_dir, settings.ollama_url, root, prompts, app.state.inference_lock
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type"],
    )

    @app.get("/health", response_model=Health, operation_id="health")
    def health() -> Health:
        """Report process readiness without loading or contacting a model."""
        return Health()

    @app.get("/setup/status", response_model=SetupStatus, operation_id="setup_status")
    def setup_status() -> dict[str, object]:
        """Return setup progress, local resources and the recommended catalog."""
        return dict(app.state.setup.snapshot())

    @app.post("/setup/skip", response_model=SetupStatus, operation_id="setup_skip")
    def setup_skip() -> dict[str, object]:
        """Choose authored fallback mode without downloading a model."""
        if not app.state.setup.skip():
            raise HTTPException(status_code=409, detail="Setup is busy")
        return dict(app.state.setup.snapshot())

    @app.post("/setup/start", response_model=SetupStatus, operation_id="setup_start")
    def setup_start(request: SetupRequest) -> dict[str, object]:
        """With explicit consent, install and check a recommended model."""
        if not app.state.setup.start(request.model):
            raise HTTPException(status_code=409, detail="Unknown model or setup is busy")
        return dict(app.state.setup.snapshot())

    @app.post("/prepare", response_model=Readiness, operation_id="prepare")
    def prepare() -> Readiness:
        """Prepare an installed, selected model or explicitly enter fallback mode."""
        with app.state.inference_lock:
            app.state.prepared = None
            model = selected_model(settings.data_dir)
            if model is not None:
                with contextlib.suppress(httpx.HTTPError, ValueError, OSError):
                    app.state.prepared = prepare_model(settings.ollama_url, model)
            return Readiness(mode="ready" if app.state.prepared else "fallback")

    @app.post("/dialogue", response_model=DialogueResponse, operation_id="dialogue")
    def dialogue(request: DialogueRequest) -> DialogueResponse:
        """Resolve an authored reply; model output is never returned to the player."""
        story: Story = load_story(resource_root() / "content")
        obj = next((item for item in story.objects if item.id == request.object_id), None)
        ids = {item.id for item in story.objects}
        if (
            obj is None
            or not set(request.recovered) <= ids
            or len(set(request.recovered)) != len(request.recovered)
        ):
            raise HTTPException(status_code=422, detail="Invalid object or recovery state")
        if not request.message.strip():
            raise HTTPException(status_code=422, detail="Message is empty")
        with app.state.inference_lock:
            prepared: PreparedModel | None = app.state.prepared
            if prepared is None:
                line = (
                    obj.fallbacks.recovered if obj.id in request.recovered else obj.fallbacks.error
                )
                return DialogueResponse(
                    relevant=None, reply=getattr(line, request.language), fallback_used=True
                )
            result = interpret(
                story,
                obj.id,
                set(request.recovered),
                request.language,
                request.message,
                origin=settings.ollama_url,
                model=prepared.model,
                prompts=resource_root() / "api" / "prompts"
                if not getattr(sys, "frozen", False)
                else resource_root() / "prompts",
                think=prepared.think,
            )
            return DialogueResponse(
                relevant=result.relevant, reply=result.reply, fallback_used=result.fallback_used
            )

    return app
