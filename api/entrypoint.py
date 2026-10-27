"""PyInstaller entry point.

Kept separate from `app/__main__.py` so the frozen binary has a single, import-safe module to
start from, and so multiprocessing on Windows does not re-run the server on spawn.
"""

import multiprocessing
import threading

import psutil
import uvicorn

from app.config import Settings
from app.main import create_app


def main() -> None:
    settings = Settings.model_validate({})
    server = uvicorn.Server(
        uvicorn.Config(
            create_app(settings),
            host=settings.host,
            port=settings.port,
            log_level="warning",
            access_log=False,
        )
    )
    if settings.parent_pid is not None:
        parent = psutil.Process(settings.parent_pid)

        def watch_parent() -> None:
            try:
                while parent.is_running() and parent.status() != psutil.STATUS_ZOMBIE:
                    threading.Event().wait(1)
            except psutil.NoSuchProcess:
                pass
            server.should_exit = True

        threading.Thread(target=watch_parent, daemon=True).start()
    server.run()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
