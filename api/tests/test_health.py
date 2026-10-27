from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.config import Settings
from app.main import create_app


def settings(tmp_path: Path, **overrides: object) -> Settings:
    values: dict[str, object] = {
        "port": 8765,
        "data_dir": tmp_path,
        "ollama_url": "http://127.0.0.1:11500",
        "cors_origins": ["app://last-candle"],
        **overrides,
    }
    return Settings.model_validate(values)


def test_health_needs_no_model(tmp_path: Path) -> None:
    with TestClient(create_app(settings(tmp_path))) as client:
        assert client.get("/health").json() == {"status": "ok"}


def test_cors_refuses_untrusted_websites(tmp_path: Path) -> None:
    with TestClient(create_app(settings(tmp_path))) as client:
        trusted = client.get("/health", headers={"Origin": "app://last-candle"})
        assert trusted.headers["access-control-allow-origin"] == "app://last-candle"
        untrusted = client.get("/health", headers={"Origin": "https://example.com"})
        assert "access-control-allow-origin" not in untrusted.headers


@pytest.mark.parametrize(
    "url",
    [
        "https://ollama.com",
        "http://0.0.0.0:11434",
        "http://127.0.0.1@evil.com",
        "http://127.0.0.1/a",
    ],
)
def test_refuses_remote_engine(tmp_path: Path, url: str) -> None:
    with pytest.raises(ValidationError):
        settings(tmp_path, ollama_url=url)


def test_entrypoint_reads_required_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("CANDLE_PORT", "54321")
    monkeypatch.setenv("CANDLE_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("CANDLE_OLLAMA_URL", "http://127.0.0.1:12345")
    loaded = Settings.model_validate({})
    assert loaded.port == 54321
    assert loaded.data_dir == tmp_path
