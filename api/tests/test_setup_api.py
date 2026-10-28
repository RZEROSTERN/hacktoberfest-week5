"""Exercise the real HTTP client against a local Ollama protocol stand-in."""

import json
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@contextmanager
def engine(*, fail_pull: bool = False) -> Iterator[tuple[int, list[str]]]:
    calls: list[str] = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            pass

        def respond(self, value: object) -> None:
            data = json.dumps(value).encode() + b"\n"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:
            calls.append(self.path)
            if self.path == "/api/tags":
                self.respond({"models": []})
            elif self.path == "/api/ps":
                self.respond({"models": [{"name": "qwen3.5:0.8b"}]})
            else:
                self.send_error(501)

        def do_POST(self) -> None:
            calls.append(self.path)
            body: dict[str, Any] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if self.path == "/api/pull":
                self.respond({"error": "network failure"} if fail_pull else {"status": "success"})
            elif self.path == "/api/show":
                self.respond({"capabilities": []})
            elif self.path == "/api/generate":
                self.respond({"done": True})
            elif self.path == "/api/chat":
                properties = body["format"]["properties"]
                answer = (
                    {"relevant": True}
                    if "relevant" in properties
                    else {"reply_id": properties["reply_id"]["enum"][0]}
                )
                self.respond({"message": {"content": json.dumps(answer)}, "done": True})
            else:
                self.send_error(501)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.server_port, calls
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def client_for(directory: Path, port: int) -> TestClient:
    return TestClient(
        create_app(
            Settings.model_validate(
                {
                    "port": 8765,
                    "data_dir": directory,
                    "ollama_url": f"http://127.0.0.1:{port}",
                }
            )
        )
    )


def wait_for_result(client: TestClient) -> dict[str, Any]:
    for _ in range(100):
        status: dict[str, Any] = client.get("/setup/status").json()
        if status["state"] in {"ready", "failed"}:
            return status
        time.sleep(0.02)
    raise AssertionError("setup did not finish")


def test_consent_download_and_compatibility(tmp_path: Path) -> None:
    with engine() as (port, calls), client_for(tmp_path, port) as client:
        initial = client.get("/setup/status").json()
        tag = initial["models"][0]["tag"]
        assert initial["setup_complete"] is False
        assert client.post("/setup/start", json={"model": tag, "consent": False}).status_code == 422
        assert (
            client.post("/setup/start", json={"model": "other", "consent": True}).status_code == 409
        )
        assert calls == []
        assert client.post("/setup/start", json={"model": tag, "consent": True}).status_code == 200
        status = wait_for_result(client)
        assert status["state"] == "ready"
        assert status["selected_model"] == tag
        assert status["setup_complete"] is True
        assert calls.count("/api/pull") == 1
        assert calls.count("/api/chat") == 2
        assert json.loads((tmp_path / "settings.json").read_text())["model"] == tag


def test_failed_download_and_skip_do_not_select_a_model(tmp_path: Path) -> None:
    with engine(fail_pull=True) as (port, calls), client_for(tmp_path, port) as client:
        tag = client.get("/setup/status").json()["models"][0]["tag"]
        client.post("/setup/start", json={"model": tag, "consent": True})
        status = wait_for_result(client)
        assert status["state"] == "failed"
        assert status["setup_complete"] is False
        assert not (tmp_path / "settings.json").exists()
        assert "/api/pull" in calls
        assert client.post("/setup/skip").json()["setup_complete"] is True
        assert json.loads((tmp_path / "settings.json").read_text())["model"] is None
