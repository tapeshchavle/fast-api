"""
Application configuration using Pydantic Settings.

All config is loaded from environment variables / .env file.
Add new settings here as the project grows.
"""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────
    app_name: str = "FastAPI App"
    app_version: str = "0.1.0"
    debug: bool = False

    # ── Server ───────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000

    # ── CORS ─────────────────────────────────────────────────
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ── Database (uncomment when ready) ──────────────────────
    # database_url: str = "sqlite+aiosqlite:///./app.db"

    # ── Auth (uncomment when ready) ──────────────────────────
    # secret_key: str = "change-me"
    # access_token_expire_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — resolved once per process."""
    return Settings()
