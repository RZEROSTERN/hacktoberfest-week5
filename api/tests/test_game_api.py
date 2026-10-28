import json
import socket
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def client_for(directory: Path, port: int = 11500) -> TestClient:
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


def test_fallback_is_authored_and_rejects_invalid_requests(tmp_path: Path) -> None:
    with client_for(tmp_path) as client:
        assert client.post("/prepare").json() == {"mode": "fallback"}
        payload = {
            "object_id": "radio",
            "recovered": [],
            "language": "en",
            "message": "I hear static",
        }
        response = client.post("/dialogue", json=payload)
        assert response.status_code == 200
        assert response.json() == {
            "relevant": None,
            "reply": "The silence need not be empty. We can listen together a moment.",
            "fallback_used": True,
        }
        for change in (
            {"object_id": "unknown"},
            {"recovered": ["radio", "radio"]},
            {"message": "  "},
            {"extra": 1},
        ):
            assert client.post("/dialogue", json={**payload, **change}).status_code == 422


def test_unreachable_engine_falls_back_without_downloading(tmp_path: Path) -> None:
    (tmp_path / "settings.json").write_text(json.dumps({"model": "test-model"}))
    with socket.socket() as unused:
        unused.bind(("127.0.0.1", 0))
        with client_for(tmp_path, unused.getsockname()[1]) as client:
            assert client.post("/prepare").json() == {"mode": "fallback"}
