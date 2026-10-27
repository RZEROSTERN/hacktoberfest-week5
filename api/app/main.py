"""Small local API; narrative endpoints arrive after story approval and the spike."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import Settings


class Health(BaseModel):
    status: str = "ok"


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="The Last Candle local API", version="0.1.0")
    app.state.settings = settings
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

    return app
