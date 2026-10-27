"""Environment contract shared by development and the packaged executable."""

from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CANDLE_")

    host: Literal["127.0.0.1"] = "127.0.0.1"
    port: int = Field(ge=1, le=65535)
    data_dir: Path
    ollama_url: str
    cors_origins: list[str] = []
    parent_pid: int | None = Field(default=None, gt=0)

    @field_validator("ollama_url")
    @classmethod
    def local_engine_only(cls, value: str) -> str:
        parsed = urlparse(value)
        if (
            parsed.scheme != "http"
            or parsed.hostname != "127.0.0.1"
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path not in ("", "/")
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("Ollama must use a local loopback HTTP origin")
        return value.rstrip("/")
