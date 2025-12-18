from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.context import request_context_middleware
from app.api.errors import register_exception_handlers
from app.api.v1.router import router as api_v1_router
from app.core.config import get_settings
from app.core.logging.config import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()
    app = FastAPI(title=settings.app_name, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware("http")(request_context_middleware())
    register_exception_handlers(app)
    app.include_router(api_v1_router, prefix=settings.api_prefix)
    return app


app = create_app()
