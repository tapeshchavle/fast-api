"""
Health check endpoint.

Used by load balancers, container orchestrators (K8s),
and monitoring systems to verify service availability.
"""

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter()


@router.get(
    "",
    summary="Health Check",
    description="Returns the health status of the application.",
)
async def health_check() -> dict:
    """Basic health check — returns app name, version, and status."""
    settings = get_settings()
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
    }
