"""Awesome FastAPI service module."""

from importlib.metadata import version

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

APP_VERSION = version("awesome-playground")
router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str


class MessageResponse(BaseModel):
    """Message response model."""

    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse: Service health status.
    """
    return HealthResponse(status="healthy", version=APP_VERSION)


@router.get("/", response_model=MessageResponse)
async def root() -> MessageResponse:
    """Root endpoint.

    Returns:
        MessageResponse: Welcome message.
    """
    return MessageResponse(message="Welcome to Awesome Service!")


@router.get("/items/{item_id}", response_model=MessageResponse)
async def read_item(item_id: int) -> MessageResponse:
    """Read item by ID.

    Args:
        item_id: The item identifier.

    Returns:
        MessageResponse: Item message.

    Raises:
        HTTPException: If item_id is less than 1.
    """
    if item_id < 1:
        raise HTTPException(status_code=400, detail="Item ID must be >= 1")
    return MessageResponse(message=f"Item {item_id}")


def create_app() -> FastAPI:
    application = FastAPI(
        title="Awesome Service",
        description="A basic FastAPI service for awesome-playground",
        version=APP_VERSION,
    )
    application.include_router(router)
    return application


app = create_app()

__all__ = ["HealthResponse", "MessageResponse", "app", "create_app"]
