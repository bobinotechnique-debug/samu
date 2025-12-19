import functools
from typing import Literal

from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

DEFAULT_DATABASE_URL = "sqlite+pysqlite:///:memory:"
DEFAULT_REDIS_URL = "redis://localhost:6379/0"


Environment = Literal["local", "ci", "staging", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SAMU_",
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        extra="forbid",
    )

    app_name: str = Field(default="Samu Backend")
    environment: Environment = Field(default="local")
    debug: bool = Field(default=False)
    testing: bool = Field(default=False)
    database_url: str = Field(default=DEFAULT_DATABASE_URL)
    redis_url: str = Field(default=DEFAULT_REDIS_URL)
    api_prefix: str = Field(default="/api/v1")
    request_timeout_seconds: int = Field(default=30, gt=0)
    cors_origins: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_required_settings(self) -> "Settings":
        if self.environment in {"ci", "staging", "production"} and not self.testing:
            missing: list[str] = []
            if self.database_url == DEFAULT_DATABASE_URL:
                missing.append("database_url")
            if self.redis_url == DEFAULT_REDIS_URL:
                missing.append("redis_url")
            if missing:
                joined = ", ".join(missing)
                raise ValueError(f"Missing required runtime settings for {self.environment}: {joined}")
        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type["Settings"],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, dotenv_settings, init_settings, file_secret_settings


@functools.lru_cache(maxsize=1)
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(f"Invalid configuration: {exc}") from exc
