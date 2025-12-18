import functools
from typing import Literal

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


Environment = Literal["local", "ci", "staging", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SAMU_", env_file=".env", extra="forbid")

    app_name: str = Field(default="Samu Backend")
    environment: Environment = Field(default="local")
    debug: bool = Field(default=False)
    testing: bool = Field(default=False)
    database_url: str
    redis_url: str
    api_prefix: str = Field(default="/api/v1")
    request_timeout_seconds: int = Field(default=30, gt=0)
    cors_origins: list[str] = Field(default_factory=list)


@functools.lru_cache(maxsize=1)
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(f"Invalid configuration: {exc}") from exc
