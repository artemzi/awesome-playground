"""Application configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment/.env file."""

    model_config = SettingsConfigDict(
        env_prefix="AWESOME_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    host: str = "0.0.0.0"  # noqa: S104  # nosec B104
    port: int = 8000
    log_level: str = "INFO"
    debug: bool = False
    cors_origins: list[str] = ["*"]


settings = Settings()
