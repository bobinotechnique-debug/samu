from fastapi import APIRouter

from app.api.routes.health import compatibility_router as health_compatibility_router

router = APIRouter()
router.include_router(health_compatibility_router, prefix="/health", tags=["health"])
