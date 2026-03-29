"""Tests for the health check endpoint."""

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """GET /api/v1/health returns 200 with status healthy."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data
