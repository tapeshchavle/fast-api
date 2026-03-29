"""
Shared test fixtures.

The `client` fixture provides an async HTTP client
wired to the FastAPI app for integration testing.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.v1.endpoints.items import reset_items_store
from app.main import create_app


@pytest.fixture(autouse=True)
def _reset_stores():
    """Reset all in-memory stores before each test for isolation."""
    reset_items_store()
    yield
    reset_items_store()


@pytest.fixture
def app():
    """Create a fresh application instance for each test."""
    return create_app()


@pytest.fixture
async def client(app):
    """Async HTTP client for testing API endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
