"""CLI entry points for awesome-playground."""

import uvicorn

from awesome_playground.config import settings


def main() -> None:
    """Run the FastAPI application using uvicorn."""
    uvicorn.run(
        "awesome_playground.awesome_service:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
