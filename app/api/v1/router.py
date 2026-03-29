"""
API v1 router — aggregates all v1 endpoint routers.

Add new feature routers here as the project grows.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, items

api_router = APIRouter()

# ── Register endpoint routers ────────────────────────────
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])

# ── Add more routers below ──────────────────────────────
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
