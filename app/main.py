"""
FastAPI application factory.

Creates and configures the FastAPI app instance with middleware,
exception handlers, and routers.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.v1.router import api_router
from app.core.exceptions import register_exception_handlers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan handler.

    Use this to initialize and tear down resources like:
    - Database connection pools
    - Redis connections
    - ML model loading
    - Background task schedulers
    """
    settings = get_settings()
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)

    # ── Startup ──────────────────────────────────────────
    # e.g. await database.connect()
    yield
    # ── Shutdown ─────────────────────────────────────────
    # e.g. await database.disconnect()
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Application factory — builds and returns a configured FastAPI instance."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ── Middleware ────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception handlers ───────────────────────────────
    register_exception_handlers(app)

    # ── Routers ──────────────────────────────────────────
    app.include_router(api_router, prefix="/api/v1")

    return app
