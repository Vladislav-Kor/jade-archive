from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional, List
import re

# ============================================
# Базовые схемы
# ============================================

class SocialMediaBase(BaseModel):
    platform: str
    link: str

class SocialMediaResponse(SocialMediaBase):
    id: int
    class Config:
        from_attributes = True

class TagPreferenceBase(BaseModel):
    category: str
    value: str

class TagPreferenceResponse(TagPreferenceBase):
    id: int
    class Config:
        from_attributes = True

# ============================================
# Digital Account Schemas (ДО PersonResponse)
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
    
    # Игровые ID и идентификаторы
    account_id: Optional[str] = None
    uid: Optional[str] = None
    user_id: Optional[str] = None
    friend_code: Optional[str] = None
    server_id: Optional[str] = None
    server_name: Optional[str] = None
    region: Optional[str] = None
    
    # Игровые данные
    nickname: Optional[str] = None
    server: Optional[str] = None
    level: Optional[int] = None
    rank: Optional[str] = None
    guild: Optional[str] = None
    characters: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = True

class DigitalAccountCreate(DigitalAccountBase):
    pass

class DigitalAccountUpdate(DigitalAccountBase):
    pass

class DigitalAccountResponse(DigitalAccountBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============================================
# Person Schema
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
    importance: Optional[float] = 0.0
    importance_level: Optional[str] = "medium"
    notes: Optional[str] = None

    @field_validator('children_count', mode='before')
    @classmethod
    def validate_children_count(cls, v):
        if v is None or v == '':
            return 0
        try:
            return int(v)
        except (ValueError, TypeError):
            return 0

    @field_validator('height', 'weight', 'shoe_size', 'chest_size', 'waist_size', 'hip_size', 'heart_rate', mode='before')
    @classmethod
    def validate_numeric_fields(cls, v):
        if v is None or v == '':
            return None
        try:
            return int(v)
        except (ValueError, TypeError):
            return None

    @field_validator('importance', mode='before')
    @classmethod
    def validate_importance(cls, v):
        if v is None or v == '':
            return 0.0
        try:
            return float(v)
        except (ValueError, TypeError):
            return 0.0

    @field_validator('birth_date', mode='before')
    @classmethod
    def validate_birth_date(cls, v):
        if v is None or v == '':
            return None
        return v

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Полное имя не может быть пустым')
        if len(v) > 255:
            raise ValueError('Полное имя не может превышать 255 символов')
        return v.strip()

    @field_validator('short_name')
    @classmethod
    def validate_short_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Короткое имя не может быть пустым')
        if len(v) > 100:
            raise ValueError('Короткое имя не может превышать 100 символов')
        if not re.match(r'^[a-zA-Zа-яА-Я0-9_-]+$', v):
            raise ValueError('Короткое имя может содержать только буквы (русские или английские), цифры, дефис и подчеркивание')
        return v.strip()

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None or v == '':
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
            raise ValueError('Неверный формат телефона')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is None or v == '':
            return None
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Неверный формат email')
        return v.lower()

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v is None or v == '':
            return None
        valid_genders = ['male', 'female', 'other']
        if v not in valid_genders:
            raise ValueError('Пол должен быть "male", "female" или "other"')
        return v

class PersonCreate(PersonBase):
    pass

class PersonUpdate(PersonBase):
    pass

class PersonResponse(PersonBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    social_media: List[SocialMediaResponse] = []
    tags_prefs: List[TagPreferenceResponse] = []
    digital_accounts: List[DigitalAccountResponse] = []  # Теперь DigitalAccountResponse определён
    
    class Config:
        from_attributes = True

# ============================================
# Relation Schemas
# ============================================

class RelationBase(BaseModel):
    parent_id: int
    child_id: int
    relation_type: str

class RelationCreate(RelationBase):
    @field_validator('relation_type')
    @classmethod
    def validate_relation_type(cls, v):
        if not v or not v.strip():
            raise ValueError('Тип связи не может быть пустым')
        if len(v) > 100:
            raise ValueError('Тип связи не может превышать 100 символов')
        return v.strip()

class RelationResponse(RelationBase):
    id: int
    class Config:
        from_attributes = True

# ============================================
# Tree Node Schema
# ============================================

class TreeNode(BaseModel):
    id: int
    name: str
    short_name: str
    importance: float
    importance_level: str
    children: List['TreeNode'] = []

TreeNode.model_rebuild()