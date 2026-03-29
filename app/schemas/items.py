"""
Pydantic schemas for the Items domain.

Schemas are split by purpose:
- Base: shared fields
- Create: fields for creating a resource
- Update: fields for partial updates
- Response: fields returned to the client
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Shared item properties."""

    name: str = Field(..., min_length=1, max_length=255, examples=["Widget"])
    description: Optional[str] = Field(None, max_length=1000, examples=["A useful widget"])
    price: float = Field(..., gt=0, examples=[29.99])


class ItemCreate(ItemBase):
    """Schema for creating a new item."""

    pass


class ItemUpdate(BaseModel):
    """Schema for partial updates — all fields optional."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)


class ItemResponse(ItemBase):
    """Schema returned to the client."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ItemListResponse(BaseModel):
    """Paginated list of items."""

    items: List[ItemResponse]
    total: int
    page: int
    page_size: int
