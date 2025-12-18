from fastapi import APIRouter

from app.api.v1.routes import collaborators, finance, health, notifications, orgs, planning, projects

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(orgs.router, prefix="/orgs", tags=["orgs"])
router.include_router(projects.router, prefix="/projects", tags=["projects"])
router.include_router(collaborators.router, prefix="/collaborators", tags=["collaborators"])
router.include_router(planning.router, prefix="/planning", tags=["planning"])
router.include_router(finance.router, prefix="/finance", tags=["finance"])
router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
