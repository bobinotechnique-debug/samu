from datetime import datetime, timezone
from typing import Callable, Literal

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from app.api.deps import get_app_settings
from app.core.config import Settings
from app.core.db.session import check_database


class HealthResponse(BaseModel):
    status: Literal["ok", "error"]
    timestamp: str
    checks: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


health_router = APIRouter(prefix="/health", tags=["health"])
compatibility_router = APIRouter()


HealthChecks = dict[str, str]
ReadinessChecker = Callable[[], HealthChecks]


def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_readiness_checker() -> HealthChecks:
    checks: HealthChecks = {}
    try:
        check_database()
        checks["db"] = "ok"
    except Exception:
        checks["db"] = "error"
    return checks


def get_readiness_checker(settings: Settings = Depends(get_app_settings)) -> ReadinessChecker:
    if settings.testing:
        return lambda: {"db": "ok"}
    return default_readiness_checker


def build_health_response(checks: HealthChecks | None = None) -> HealthResponse:
    checks = checks or {}
    has_error = any(result != "ok" for result in checks.values())
    status_value: Literal["ok", "error"] = "error" if has_error else "ok"
    return HealthResponse(status=status_value, timestamp=current_timestamp(), checks=checks)


def readiness_response(readiness_checker: ReadinessChecker) -> JSONResponse:
    checks = readiness_checker()
    response = build_health_response(checks)
    status_code = (
        status.HTTP_200_OK if response.status == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return JSONResponse(status_code=status_code, content=response.model_dump(exclude_none=True))


@health_router.get("/live", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def live() -> HealthResponse:
    return build_health_response({})


@health_router.get("/ready", response_model=HealthResponse)
def ready(readiness_checker: ReadinessChecker = Depends(get_readiness_checker)) -> JSONResponse:
    return readiness_response(readiness_checker)


@compatibility_router.get("", response_model=HealthResponse, tags=["health"])
def readiness_alias(
    readiness_checker: ReadinessChecker = Depends(get_readiness_checker),
) -> JSONResponse:
    return readiness_response(readiness_checker)
