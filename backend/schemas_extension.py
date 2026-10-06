from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Any

class CategoryBase(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_system: bool = False
    sort_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_system: Optional[bool] = None
    sort_order: Optional[int] = None

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    children: List['CategoryResponse'] = []
    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str
    slug: str
    color: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

from schemas import (
    CrossRecordBase, CrossRecordCreate, CrossRecordUpdate, CrossRecordResponse,
    PartnerBase, PartnerCreate, PartnerUpdate, PartnerResponse,
    DeviceBase, DeviceCreate, DeviceUpdate, DeviceResponse,
    CategoryBase, CategoryCreate, CategoryUpdate, CategoryResponse,
    TagBase, TagCreate, TagUpdate, TagResponse
)

class PartnerBase(BaseModel):
    person_id: int
    partner_id: int
    relationship_type: Optional[str] = None
    relationship_status: Optional[str] = None
    relationship_label: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    breakup_reason: Optional[str] = None
    emotional_connection: Optional[str] = None
    physical_connection: Optional[str] = None
    relationship_rating: Optional[int] = None
    relationship_notes: Optional[str] = None

class PartnerCreate(PartnerBase):
    pass

class PartnerResponse(PartnerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    person_id: int
    device_type: str
    brand: str
    model: str
    color: Optional[str] = None
    specs: Optional[str] = None
    imei: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = None
    purchase_place: Optional[str] = None
    warranty_until: Optional[date] = None
    accessories: Optional[str] = None
    condition: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True

class DeviceCreate(DeviceBase):
    pass

class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
