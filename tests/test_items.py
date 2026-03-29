"""Tests for the Items CRUD endpoints."""

import pytest


@pytest.mark.asyncio
async def test_create_item(client):
    """POST /api/v1/items creates and returns an item."""
    payload = {"name": "Test Widget", "description": "A test item", "price": 9.99}
    response = await client.post("/api/v1/items", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Widget"
    assert data["price"] == 9.99
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_list_items(client):
    """GET /api/v1/items returns a paginated list."""
    # Create some items first
    for i in range(3):
        await client.post("/api/v1/items", json={"name": f"Item {i}", "price": 10.0 + i})

    response = await client.get("/api/v1/items")
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3
    assert data["page"] == 1


@pytest.mark.asyncio
async def test_get_item(client):
    """GET /api/v1/items/{id} returns a single item."""
    create_resp = await client.post("/api/v1/items", json={"name": "Fetch Me", "price": 5.0})
    item_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Fetch Me"


@pytest.mark.asyncio
async def test_get_item_not_found(client):
    """GET /api/v1/items/999 returns 404."""
    response = await client.get("/api/v1/items/999")
    assert response.status_code == 404
    assert response.json()["error_type"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_update_item(client):
    """PATCH /api/v1/items/{id} partially updates an item."""
    create_resp = await client.post("/api/v1/items", json={"name": "Old Name", "price": 1.0})
    item_id = create_resp.json()["id"]

    response = await client.patch(f"/api/v1/items/{item_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["price"] == 1.0  # unchanged


@pytest.mark.asyncio
async def test_delete_item(client):
    """DELETE /api/v1/items/{id} removes the item."""
    create_resp = await client.post("/api/v1/items", json={"name": "Delete Me", "price": 1.0})
    item_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_resp = await client.get(f"/api/v1/items/{item_id}")
    assert get_resp.status_code == 404
