from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.api.deps import get_app_settings
from app.core.config import Settings
from app.core.db.session import check_database


class HealthResponse(BaseModel):
    status: str


health_router = APIRouter(prefix="/health", tags=["health"])
compatibility_router = APIRouter()


def readiness_dependency(settings: Settings = Depends(get_app_settings)) -> None:
    if settings.testing:
        return
    check_database()


@health_router.get("/live", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def live() -> HealthResponse:
    return HealthResponse(status="live")


@health_router.get("/ready", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def ready(_: None = Depends(readiness_dependency)) -> HealthResponse:
    return HealthResponse(status="ready")


@compatibility_router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
)
def readiness_alias(_: None = Depends(readiness_dependency)) -> HealthResponse:
    return HealthResponse(status="ready")
