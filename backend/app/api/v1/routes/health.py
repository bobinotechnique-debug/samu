from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.api.deps import get_app_settings
from app.core.config import Settings
from app.core.db.session import check_database

router = APIRouter()


class HealthResponse(BaseModel):
    status: str


@router.get("/live", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def live() -> HealthResponse:
    return HealthResponse(status="live")


@router.get("/ready", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def ready(settings: Settings = Depends(get_app_settings)) -> HealthResponse:
    if settings.testing:
        return HealthResponse(status="ready")
    check_database()
    return HealthResponse(status="ready")
