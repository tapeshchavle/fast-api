"""
Shared dependency injection functions.

Use these with FastAPI's Depends() to inject common resources
into route handlers (settings, DB sessions, current user, etc.).
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.config import Settings, get_settings

# Type alias for injecting settings
SettingsDep = Annotated[Settings, Depends(get_settings)]


# ── Add more dependencies below as the project grows ─────
#
# Example: Database session dependency
#
# async def get_db() -> AsyncIterator[AsyncSession]:
#     async with async_session_maker() as session:
#         yield session
#
# DbSession = Annotated[AsyncSession, Depends(get_db)]
#
# Example: Current user dependency
#
# async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
#     ...
#
# CurrentUser = Annotated[User, Depends(get_current_user)]
