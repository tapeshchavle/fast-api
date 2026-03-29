"""
Items CRUD endpoints.

Uses an in-memory store for now — swap in a real database
service layer when you're ready. The endpoint signatures
and schemas stay the same.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from fastapi import APIRouter, Query

from app.core.exceptions import NotFoundException
from app.schemas.items import ItemCreate, ItemListResponse, ItemResponse, ItemUpdate

router = APIRouter()

# ── In-memory store (replace with DB service later) ──────
_items_db: Dict[int, dict] = {}
_next_id: int = 1


def reset_items_store() -> None:
    """Reset the in-memory store — used by tests for isolation."""
    global _next_id
    _items_db.clear()
    _next_id = 1


def _get_now() -> datetime:
    return datetime.now(timezone.utc)


# ── Endpoints ────────────────────────────────────────────


@router.get(
    "",
    response_model=ItemListResponse,
    summary="List Items",
    description="Retrieve a paginated list of all items.",
)
async def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
) -> ItemListResponse:
    """List items with pagination."""
    all_items = list(_items_db.values())
    total = len(all_items)

    start = (page - 1) * page_size
    end = start + page_size
    page_items = all_items[start:end]

    return ItemListResponse(
        items=[ItemResponse(**item) for item in page_items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post(
    "",
    response_model=ItemResponse,
    status_code=201,
    summary="Create Item",
    description="Create a new item.",
)
async def create_item(payload: ItemCreate) -> ItemResponse:
    """Create a new item and return it."""
    global _next_id
    now = _get_now()

    item = {
        "id": _next_id,
        **payload.model_dump(),
        "created_at": now,
        "updated_at": now,
    }
    _items_db[_next_id] = item
    _next_id += 1

    return ItemResponse(**item)


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get Item",
    description="Retrieve a single item by ID.",
)
async def get_item(item_id: int) -> ItemResponse:
    """Get an item by its ID."""
    item = _items_db.get(item_id)
    if not item:
        raise NotFoundException(detail=f"Item with id {item_id} not found")
    return ItemResponse(**item)


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update Item",
    description="Partially update an existing item.",
)
async def update_item(item_id: int, payload: ItemUpdate) -> ItemResponse:
    """Update an item with partial data."""
    item = _items_db.get(item_id)
    if not item:
        raise NotFoundException(detail=f"Item with id {item_id} not found")

    update_data = payload.model_dump(exclude_unset=True)
    item.update(update_data)
    item["updated_at"] = _get_now()
    _items_db[item_id] = item

    return ItemResponse(**item)


@router.delete(
    "/{item_id}",
    status_code=204,
    summary="Delete Item",
    description="Delete an item by ID.",
)
async def delete_item(item_id: int) -> None:
    """Delete an item."""
    if item_id not in _items_db:
        raise NotFoundException(detail=f"Item with id {item_id} not found")
    del _items_db[item_id]
