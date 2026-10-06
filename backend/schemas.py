"""
schemas.py - Complete Pydantic schemas for Jade Archive API
Production-ready with relaxed validation for existing data
"""

from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date, datetime
from typing import Optional, List, Any, Generic, TypeVar
import re

# ============================================
# GENERIC PAGINATION
# ============================================

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    pages: int
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# RESPONSE MODELS
# ============================================

class HealthResponse(BaseModel):
    status: str
    database: str
    version: str
    timestamp: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: dict
    timestamp: str

# ============================================
# SOCIAL MEDIA SCHEMAS
# ============================================

class SocialMediaBase(BaseModel):
    platform: str
    link: str
    
    @field_validator('platform')
    @classmethod
    def validate_platform(cls, v):
        if not v or not v.strip():
            return 'other'
        platform = v.strip().lower()
        allowed_platforms = ['telegram', 'whatsapp', 'viber', 'signal', 'instagram', 'facebook', 'twitter', 'linkedin', 'youtube', 'tiktok', 'vk', 'ok', 'wechat', 'line', 'discord', 'reddit', 'pinterest', 'snapchat', 'github', 'steam', 'max', 'imo', 'snapchat', 'other']
        if platform not in allowed_platforms:
            return 'other'
        return platform
    
    @field_validator('link')
    @classmethod
    def validate_link(cls, v):
        if not v or not v.strip():
            return v
        link = v.strip()
        if not link.startswith(('http://', 'https://')):
            link = 'https://' + link
        return link

class SocialMediaResponse(SocialMediaBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# TAG PREFERENCES SCHEMAS
# ============================================

class TagPreferenceBase(BaseModel):
    category: str
    value: str

class TagPreferenceResponse(TagPreferenceBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# DIGITAL ACCOUNTS SCHEMAS
# ============================================

class DigitalAccountBase(BaseModel):
    platform_type: str
    platform_name: str
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    backup_codes: Optional[str] = None
    security_questions: Optional[str] = None
    account_id: Optional[str] = None
    uid: Optional[str] = None
    user_id: Optional[str] = None
    friend_code: Optional[str] = None
    server_id: Optional[str] = None
    server_name: Optional[str] = None
    region: Optional[str] = None
    nickname: Optional[str] = None
    server: Optional[str] = None
    level: Optional[int] = None
    rank: Optional[str] = None
    guild: Optional[str] = None
    characters: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True
    
    @field_validator('platform_type')
    @classmethod
    def validate_platform_type(cls, v):
        if not v or not v.strip():
            return 'other'
        platform_type = v.strip().lower()
        allowed_types = ['social', 'messenger', 'gaming', 'email', 'work', 'financial', 'shopping', 'entertainment', 'steam', 'genshin', 'mobile', 'discord', 'other']
        if platform_type not in allowed_types:
            return 'other'
        return platform_type

class DigitalAccountCreate(DigitalAccountBase):
    pass

class DigitalAccountUpdate(BaseModel):
    platform_type: Optional[str] = None
    platform_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    backup_codes: Optional[str] = None
    security_questions: Optional[str] = None
    account_id: Optional[str] = None
    uid: Optional[str] = None
    user_id: Optional[str] = None
    friend_code: Optional[str] = None
    server_id: Optional[str] = None
    server_name: Optional[str] = None
    region: Optional[str] = None
    nickname: Optional[str] = None
    server: Optional[str] = None
    level: Optional[int] = None
    rank: Optional[str] = None
    guild: Optional[str] = None
    characters: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class DigitalAccountResponse(DigitalAccountBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    link: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# REAL ESTATE SCHEMAS
# ============================================

class RealEstateBase(BaseModel):
    property_type: str
    property_name: Optional[str] = None
    address: str
    total_area: Optional[float] = None
    living_area: Optional[float] = None
    land_area: Optional[float] = None
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    rooms_count: Optional[int] = None
    bathroom_count: Optional[int] = None
    balcony_count: Optional[int] = None
    ownership_type: Optional[str] = None
    ownership_percent: float = 100.0
    cadastral_number: Optional[str] = None
    registration_date: Optional[date] = None
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    mortgage_bank: Optional[str] = None
    mortgage_amount: Optional[float] = None
    mortgage_left: Optional[float] = None
    condition: Optional[str] = None
    year_built: Optional[int] = None
    renovation_year: Optional[int] = None
    notes: Optional[str] = None
    is_active: bool = True

class RealEstateCreate(RealEstateBase):
    pass

class RealEstateUpdate(BaseModel):
    property_type: Optional[str] = None
    property_name: Optional[str] = None
    address: Optional[str] = None
    total_area: Optional[float] = None
    living_area: Optional[float] = None
    land_area: Optional[float] = None
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    rooms_count: Optional[int] = None
    bathroom_count: Optional[int] = None
    balcony_count: Optional[int] = None
    ownership_type: Optional[str] = None
    ownership_percent: Optional[float] = None
    cadastral_number: Optional[str] = None
    registration_date: Optional[date] = None
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    mortgage_bank: Optional[str] = None
    mortgage_amount: Optional[float] = None
    mortgage_left: Optional[float] = None
    condition: Optional[str] = None
    year_built: Optional[int] = None
    renovation_year: Optional[int] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class RealEstateResponse(RealEstateBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# VEHICLE SCHEMAS
# ============================================

class VehicleBase(BaseModel):
    vehicle_type: str
    brand: str
    model: str
    year: Optional[int] = None
    color: Optional[str] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None
    engine_number: Optional[str] = None
    chassis_number: Optional[str] = None
    engine_capacity: Optional[float] = None
    horsepower: Optional[int] = None
    mileage: Optional[int] = None
    transmission: Optional[str] = None
    drive_type: Optional[str] = None
    fuel_type: Optional[str] = None
    ownership_type: Optional[str] = None
    registration_date: Optional[date] = None
    registration_number: Optional[str] = None
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    loan_bank: Optional[str] = None
    loan_amount: Optional[float] = None
    loan_left: Optional[float] = None
    insurance_company: Optional[str] = None
    insurance_policy: Optional[str] = None
    insurance_until: Optional[date] = None
    osago_until: Optional[date] = None
    last_maintenance: Optional[date] = None
    next_maintenance: Optional[date] = None
    maintenance_notes: Optional[str] = None
    condition: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    vehicle_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None
    engine_number: Optional[str] = None
    chassis_number: Optional[str] = None
    engine_capacity: Optional[float] = None
    horsepower: Optional[int] = None
    mileage: Optional[int] = None
    transmission: Optional[str] = None
    drive_type: Optional[str] = None
    fuel_type: Optional[str] = None
    ownership_type: Optional[str] = None
    registration_date: Optional[date] = None
    registration_number: Optional[str] = None
    purchase_price: Optional[float] = None
    current_value: Optional[float] = None
    loan_bank: Optional[str] = None
    loan_amount: Optional[float] = None
    loan_left: Optional[float] = None
    insurance_company: Optional[str] = None
    insurance_policy: Optional[str] = None
    insurance_until: Optional[date] = None
    osago_until: Optional[date] = None
    last_maintenance: Optional[date] = None
    next_maintenance: Optional[date] = None
    maintenance_notes: Optional[str] = None
    condition: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class VehicleResponse(VehicleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# CASE SCHEMAS
# ============================================

class CaseBase(BaseModel):
    case_type: str
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "active"
    due_date: Optional[datetime] = None

class CaseCreate(CaseBase):
    pass

class CaseUpdate(BaseModel):
    case_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

class CaseResponse(CaseBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# MEDICAL RECORD SCHEMAS
# ============================================

class MedicalRecordBase(BaseModel):
    record_type: str
    title: str
    description: Optional[str] = None
    record_date: Optional[datetime] = None
    doctor_name: Optional[str] = None
    attachments: Optional[str] = None
    
    @field_validator('record_type')
    @classmethod
    def validate_record_type(cls, v):
        if not v or not v.strip():
            return 'other'
        record_type = v.strip().lower()
        allowed_types = ['examination', 'diagnosis', 'treatment', 'surgery', 'vaccination', 'test', 'prescription', 'hospitalization', 'rehabilitation', 'chronic', 'other']
        if record_type not in allowed_types:
            return 'other'
        return record_type

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(BaseModel):
    record_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    record_date: Optional[datetime] = None
    doctor_name: Optional[str] = None
    attachments: Optional[str] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# CROSS RECORD SCHEMAS
# ============================================

class CrossRecordBase(BaseModel):
    title: str
    description: Optional[str] = None
    record_type: str
    primary_category_id: int
    data: Optional[Any] = None
    record_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "active"
    importance: int = 0
    is_private: bool = False
    
    @field_validator('record_type')
    @classmethod
    def validate_record_type(cls, v):
        if not v or not v.strip():
            return 'other'
        record_type = v.strip().lower()
        allowed_types = ['sex', 'medicine', 'gifts', 'skills', 'travel', 'work', 'character', 'dates', 'events', 'documents', 'finance', 'education', 'sports', 'hobbies', 'partner', 'other']
        if record_type not in allowed_types:
            return 'other'
        return record_type

class CrossRecordCreate(CrossRecordBase):
    person_id: int
    created_by: Optional[int] = None

class CrossRecordUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    record_type: Optional[str] = None
    primary_category_id: Optional[int] = None
    data: Optional[Any] = None
    record_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    importance: Optional[int] = None
    is_private: Optional[bool] = None

class CrossRecordResponse(CrossRecordBase):
    id: int
    person_id: int
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# PERSON SCHEMAS
# ============================================

class PersonBase(BaseModel):
    full_name: str
    short_name: str
    photo_path: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    clothing_size: Optional[str] = None
    shoe_size: Optional[int] = None
    chest_size: Optional[int] = None
    waist_size: Optional[int] = None
    hip_size: Optional[int] = None
    blood_type: Optional[str] = None
    rh_factor: Optional[str] = None
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None
    medications: Optional[str] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    passport_number: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    driver_license_category: Optional[str] = None
    driver_license_number: Optional[str] = None
    marital_status: Optional[str] = None
    children_count: int = 0
    education: Optional[str] = None
    profession: Optional[str] = None
    workplace: Optional[str] = None
    favorite_color: Optional[str] = None
    favorite_flowers: Optional[str] = None
    favorite_food: Optional[str] = None
    favorite_music: Optional[str] = None
    favorite_movies: Optional[str] = None
    hobbies: Optional[str] = None
    importance: float = 0.0
    importance_level: str = "medium"
    notes: Optional[str] = None
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if not v or not v.strip():
            return 'Unknown'
        return v.strip()
    
    @field_validator('short_name')
    @classmethod
    def validate_short_name(cls, v):
        if not v or not v.strip():
            return 'unknown'
        short_name = v.strip()
        return short_name

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    full_name: Optional[str] = None
    short_name: Optional[str] = None
    photo_path: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    clothing_size: Optional[str] = None
    shoe_size: Optional[int] = None
    chest_size: Optional[int] = None
    waist_size: Optional[int] = None
    hip_size: Optional[int] = None
    blood_type: Optional[str] = None
    rh_factor: Optional[str] = None
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None
    medications: Optional[str] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    passport_number: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    driver_license_category: Optional[str] = None
    driver_license_number: Optional[str] = None
    marital_status: Optional[str] = None
    children_count: Optional[int] = None
    education: Optional[str] = None
    profession: Optional[str] = None
    workplace: Optional[str] = None
    favorite_color: Optional[str] = None
    favorite_flowers: Optional[str] = None
    favorite_food: Optional[str] = None
    favorite_music: Optional[str] = None
    favorite_movies: Optional[str] = None
    hobbies: Optional[str] = None
    importance: Optional[float] = None
    importance_level: Optional[str] = None
    notes: Optional[str] = None

class PersonResponse(PersonBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    social_media: List[SocialMediaResponse] = []
    tags_prefs: List[TagPreferenceResponse] = []
    digital_accounts: List[DigitalAccountResponse] = []
    real_estate: List[RealEstateResponse] = []
    vehicles: List[VehicleResponse] = []
    cases: List[CaseResponse] = []
    medical_records: List[MedicalRecordResponse] = []
    cross_records: List[CrossRecordResponse] = []
    partners: List['PartnerResponse'] = []
    devices: List['DeviceResponse'] = []
    relations: List['RelationResponse'] = []
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# RELATION SCHEMAS
# ============================================

class RelationBase(BaseModel):
    parent_id: int
    child_id: int
    relation_type: str
    
    @field_validator('relation_type')
    @classmethod
    def validate_relation_type(cls, v):
        if not v or not v.strip():
            return 'other'
        relation_type = v.strip()
        allowed_types = ['friend', 'family', 'colleague', 'acquaintance', 'partner', 'client', 'service', 'other']
        lower_type = relation_type.lower()
        if lower_type in ['родственник', 'родственик']:
            return 'family'
        if lower_type in ['друг', 'друг детства']:
            return 'friend'
        if lower_type in ['бывшая', 'девушка']:
            return 'partner'
        if lower_type in ['наставник']:
            return 'colleague'
        if relation_type.lower() not in allowed_types:
            return 'other'
        return relation_type.lower()

class RelationCreate(RelationBase):
    pass

class RelationUpdate(BaseModel):
    relation_type: Optional[str] = None

class RelationResponse(RelationBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    direction: Optional[str] = None
    person_name: Optional[str] = None
    person_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# PARTNER SCHEMAS
# ============================================

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
    
    @field_validator('relationship_type')
    @classmethod
    def validate_relationship_type(cls, v):
        if not v or not v.strip():
            return 'other'
        rel_type = v.strip().lower()
        if rel_type in ['романтичные', 'романтические', 'романтические ']:
            return 'romantic'
        if rel_type in ['брак']:
            return 'family'
        allowed = ['romantic', 'friendship', 'family', 'professional', 'casual', 'business', 'other']
        if rel_type not in allowed:
            return 'other'
        return rel_type

class PartnerCreate(PartnerBase):
    pass

class PartnerUpdate(BaseModel):
    person_id: Optional[int] = None
    partner_id: Optional[int] = None
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

class PartnerResponse(PartnerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# DEVICE SCHEMAS
# ============================================

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
    
    @field_validator('device_type')
    @classmethod
    def validate_device_type(cls, v):
        if not v or not v.strip():
            return 'other'
        device_type = v.strip().lower()
        allowed = ['phone', 'smartphone', 'tablet', 'laptop', 'desktop', 'monitor', 'printer', 'scanner', 'server', 'router', 'switch', 'access_point', 'camera', 'dvr', 'nas', 'smart_tv', 'game_console', 'vr_headset', 'smart_watch', 'fitness_tracker', 'watch', 'headphones', 'power-bank', 'other']
        if device_type not in allowed:
            return 'other'
        return device_type
    
    @field_validator('condition')
    @classmethod
    def validate_condition(cls, v):
        if not v or not v.strip():
            return 'good'
        condition = v.strip().lower()
        allowed = ['new', 'like_new', 'excellent', 'good', 'fair', 'poor', 'needs_repair']
        if condition not in allowed:
            if condition in ['used', 'normal']:
                return 'good'
            return 'good'
        return condition

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    device_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
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
    is_active: Optional[bool] = None

class DeviceResponse(DeviceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# CATEGORY SCHEMAS
# ============================================

class CategoryBase(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# TAG SCHEMAS
# ============================================

class TagBase(BaseModel):
    name: str
    slug: str
    category_id: int
    description: Optional[str] = None
    color: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    color: Optional[str] = None

class TagResponse(TagBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============================================
# TREE NODE SCHEMAS
# ============================================

class TreeNode(BaseModel):
    id: int
    name: str
    short_name: str
    importance: float
    importance_level: str
    children: List['TreeNode'] = []
    
    model_config = ConfigDict(from_attributes=True)

# Update forward references for circular dependencies
PersonResponse.model_rebuild()
TreeNode.model_rebuild()
PaginatedResponse.model_rebuild()