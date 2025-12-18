import logging
from logging.config import dictConfig

from app.core.config import get_settings


LOG_LEVEL = "INFO"


def configure_logging() -> None:
    settings = get_settings()
    level = LOG_LEVEL if not settings.debug else "DEBUG"
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": level,
                }
            },
            "root": {"handlers": ["console"], "level": level},
        }
    )
    logging.getLogger(__name__).debug("Logging configured with level %s", level)
