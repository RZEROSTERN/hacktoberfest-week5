"""Consent-based setup for the bundled local model engine."""

import json
import shutil
import threading
from pathlib import Path
from typing import Any

import httpx
import psutil

from app.dialogue import interpret
from app.model_lifecycle import prepare_model
from app.story import load_story


class SetupFailure(Exception):
    """A setup failure safe to display as a translated code."""


class SetupManager:
    def __init__(self, data_dir: Path, origin: str, root: Path, prompts: Path, inference_lock: Any):
        self.data_dir = data_dir
        self.origin = origin
        self.root = root
        self.prompts = prompts
        self.inference_lock = inference_lock
        self.lock = threading.Lock()
        self.state = "idle"
        self.completed = 0
        self.total = 0
        self.error: str | None = None
        self.catalog: dict[str, Any] = json.loads((root / "content" / "models.json").read_text())

    def settings(self) -> dict[str, Any]:
        try:
            data = json.loads((self.data_dir / "settings.json").read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (OSError, ValueError):
            return {}

    def write_settings(self, model: str | None) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        settings = self.settings()
        settings.update({"model": model, "setup_complete": True})
        temporary = self.data_dir / "settings.json.tmp"
        temporary.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.data_dir / "settings.json")

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            settings = self.settings()
            return {
                "setup_complete": settings.get("setup_complete") is True,
                "selected_model": settings.get("model"),
                "state": self.state,
                "completed": self.completed,
                "total": self.total,
                "error": self.error,
                "models": self.catalog["models"],
                "memory_available": psutil.virtual_memory().available,
                "disk_available": shutil.disk_usage(self.data_dir).free
                if self.data_dir.exists()
                else None,
            }

    def skip(self) -> bool:
        with self.lock:
            if self.state in {"downloading", "checking"}:
                return False
            self.write_settings(None)
            self.state = "idle"
            self.error = None
            return True

    def start(self, tag: str) -> bool:
        allowed = {entry["tag"] for entry in self.catalog["models"]}
        with self.lock:
            if tag not in allowed or self.state in {"downloading", "checking"}:
                return False
            self.state = "downloading"
            self.completed = 0
            self.total = 0
            self.error = None
        threading.Thread(target=self._run, args=(tag,), daemon=True).start()
        return True

    def _run(self, tag: str) -> None:
        try:
            with self.inference_lock:
                self._install(tag)
                with self.lock:
                    self.state = "checking"
                prepared = prepare_model(self.origin, tag)
                result = interpret(
                    load_story(self.root / "content"),
                    "bowl",
                    set(),
                    "en",
                    "Who might share this meal?",
                    origin=self.origin,
                    model=tag,
                    prompts=self.prompts,
                    think=prepared.think,
                )
                if result.relevant is None or result.fallback_used:
                    raise ValueError("compatibility check failed")
                self.write_settings(tag)
            with self.lock:
                self.state = "ready"
        except Exception as error:
            with self.lock:
                self.state = "failed"
                self.error = str(error) if isinstance(error, SetupFailure) else "setup_failed"

    def _install(self, tag: str) -> None:
        timeout = httpx.Timeout(connect=5, read=120, write=30, pool=5)
        with httpx.Client(base_url=self.origin, timeout=timeout, trust_env=False) as client:
            response = client.get("/api/tags")
            response.raise_for_status()
            installed = response.json().get("models", [])
            if any(item.get("name") == tag and not item.get("remote_host") for item in installed):
                return
            model = next(item for item in self.catalog["models"] if item["tag"] == tag)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            if shutil.disk_usage(self.data_dir).free < model["download_bytes"] + 200_000_000:
                raise SetupFailure("insufficient_disk")
            layers: dict[str, tuple[int, int]] = {}
            succeeded = False
            with client.stream("POST", "/api/pull", json={"model": tag, "stream": True}) as stream:
                stream.raise_for_status()
                for line in stream.iter_lines():
                    if not line:
                        continue
                    event = json.loads(line)
                    if "error" in event:
                        raise ValueError("download failed")
                    if event.get("digest") and "total" in event:
                        layers[event["digest"]] = (
                            int(event.get("completed", 0)),
                            int(event["total"]),
                        )
                        with self.lock:
                            self.completed = sum(item[0] for item in layers.values())
                            self.total = sum(item[1] for item in layers.values())
                    if event.get("status") == "success":
                        succeeded = True
                        break
            if not succeeded:
                raise ValueError("download interrupted")
