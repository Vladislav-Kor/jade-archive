"""
models.py - Complete SQLAlchemy models for Jade Archive API
Production-ready with all relationships, indexes, and constraints
Optimized for MySQL with proper column types to avoid row size limits
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, Text, ForeignKey, Index, UniqueConstraint, JSON
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    short_name = Column(String(100), nullable=False, unique=True, index=True)
    photo_path = Column(String(500), nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    clothing_size = Column(String(50), nullable=True)
    shoe_size = Column(Integer, nullable=True)
    chest_size = Column(Integer, nullable=True)
    waist_size = Column(Integer, nullable=True)
    hip_size = Column(Integer, nullable=True)
    blood_type = Column(String(10), nullable=True)
    rh_factor = Column(String(5), nullable=True)
    allergies = Column(Text, nullable=True)
    chronic_diseases = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    blood_pressure = Column(String(50), nullable=True)
    heart_rate = Column(Integer, nullable=True)
    passport_number = Column(String(50), nullable=True)
    inn = Column(String(50), nullable=True)
    snils = Column(String(50), nullable=True)
    driver_license_category = Column(String(50), nullable=True)
    driver_license_number = Column(String(50), nullable=True)
    marital_status = Column(String(50), nullable=True)
    children_count = Column(Integer, default=0)
    education = Column(String(255), nullable=True)
    profession = Column(String(255), nullable=True)
    workplace = Column(String(255), nullable=True)
    favorite_color = Column(String(100), nullable=True)
    favorite_flowers = Column(Text, nullable=True)
    favorite_food = Column(Text, nullable=True)
    favorite_music = Column(Text, nullable=True)
    favorite_movies = Column(Text, nullable=True)
    hobbies = Column(Text, nullable=True)
    importance = Column(Float, default=0.0)
    importance_level = Column(String(20), default="medium")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    social_media = relationship("SocialMedia", back_populates="person", cascade="all, delete-orphan")
    tags_prefs = relationship("TagPreference", back_populates="person", cascade="all, delete-orphan")
    digital_accounts = relationship("DigitalAccount", back_populates="person", cascade="all, delete-orphan")
    real_estate = relationship("RealEstate", back_populates="person", cascade="all, delete-orphan")
    vehicles = relationship("Vehicle", back_populates="person", cascade="all, delete-orphan")
    cases = relationship("Case", back_populates="person", cascade="all, delete-orphan")
    medical_records = relationship("MedicalRecord", back_populates="person", cascade="all, delete-orphan")
    cross_records = relationship("CrossRecord", foreign_keys="CrossRecord.person_id", back_populates="person", cascade="all, delete-orphan")
    cross_records_created = relationship("CrossRecord", foreign_keys="CrossRecord.created_by", back_populates="creator", cascade="all, delete-orphan")
    partners = relationship("Partner", foreign_keys="Partner.person_id", back_populates="person", cascade="all, delete-orphan")
    partner_of = relationship("Partner", foreign_keys="Partner.partner_id", back_populates="partner_person", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="person", cascade="all, delete-orphan")
    relations_as_parent = relationship("Relation", foreign_keys="Relation.parent_id", back_populates="parent", cascade="all, delete-orphan")
    relations_as_child = relationship("Relation", foreign_keys="Relation.child_id", back_populates="child", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_person_full_name", "full_name"),
        Index("idx_person_short_name", "short_name"),
        Index("idx_person_email", "email"),
        Index("idx_person_phone", "phone"),
        Index("idx_person_importance", "importance"),
    )

class SocialMedia(Base):
    __tablename__ = "social_media"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    link = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="social_media")
    
    __table_args__ = (
        UniqueConstraint("person_id", "platform", "link", name="uq_social_media_person_platform_link"),
        Index("idx_social_media_platform", "platform"),
        Index("idx_social_media_person_id", "person_id"),
    )

class TagPreference(Base):
    __tablename__ = "tag_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    value = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    person = relationship("Person", back_populates="tags_prefs")
    
    __table_args__ = (
        UniqueConstraint("person_id", "category", "value", name="uq_tag_pref_person_category_value"),
        Index("idx_tag_pref_category", "category"),
        Index("idx_tag_pref_person_id", "person_id"),
    )

class DigitalAccount(Base):
    __tablename__ = "digital_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    platform_type = Column(String(50), nullable=False)
    platform_name = Column(String(100), nullable=False)
    username = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    password = Column(Text, nullable=True)
    backup_codes = Column(Text, nullable=True)
    security_questions = Column(Text, nullable=True)
    account_id = Column(String(255), nullable=True)
    uid = Column(String(255), nullable=True)
    user_id = Column(String(255), nullable=True)
    friend_code = Column(String(50), nullable=True)
    server_id = Column(String(100), nullable=True)
    server_name = Column(String(255), nullable=True)
    region = Column(String(100), nullable=True)
    nickname = Column(String(255), nullable=True)
    server = Column(String(255), nullable=True)
    level = Column(Integer, nullable=True)
    rank = Column(String(100), nullable=True)
    guild = Column(String(255), nullable=True)
    characters = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="digital_accounts")
    
    __table_args__ = (
        Index("idx_digital_account_person_id", "person_id"),
        Index("idx_digital_account_platform_type", "platform_type"),
        Index("idx_digital_account_platform_name", "platform_name"),
        Index("idx_digital_account_is_active", "is_active"),
    )

class RealEstate(Base):
    __tablename__ = "real_estate"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    property_type = Column(String(50), nullable=False)
    property_name = Column(String(255), nullable=True)
    address = Column(Text, nullable=False)
    total_area = Column(Float, nullable=True)
    living_area = Column(Float, nullable=True)
    land_area = Column(Float, nullable=True)
    floor = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    rooms_count = Column(Integer, nullable=True)
    bathroom_count = Column(Integer, nullable=True)
    balcony_count = Column(Integer, nullable=True)
    ownership_type = Column(String(50), nullable=True)
    ownership_percent = Column(Float, default=100.0)
    cadastral_number = Column(String(100), nullable=True)
    registration_date = Column(Date, nullable=True)
    purchase_price = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    mortgage_bank = Column(String(255), nullable=True)
    mortgage_amount = Column(Float, nullable=True)
    mortgage_left = Column(Float, nullable=True)
    condition = Column(String(50), nullable=True)
    year_built = Column(Integer, nullable=True)
    renovation_year = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="real_estate")
    
    __table_args__ = (
        Index("idx_real_estate_person_id", "person_id"),
        Index("idx_real_estate_property_type", "property_type"),
        Index("idx_real_estate_is_active", "is_active"),
    )

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_type = Column(String(50), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=True)
    color = Column(String(50), nullable=True)
    license_plate = Column(String(20), nullable=True)
    vin = Column(String(17), nullable=True)
    engine_number = Column(String(50), nullable=True)
    chassis_number = Column(String(50), nullable=True)
    engine_capacity = Column(Float, nullable=True)
    horsepower = Column(Integer, nullable=True)
    mileage = Column(Integer, nullable=True)
    transmission = Column(String(50), nullable=True)
    drive_type = Column(String(50), nullable=True)
    fuel_type = Column(String(50), nullable=True)
    ownership_type = Column(String(50), nullable=True)
    registration_date = Column(Date, nullable=True)
    registration_number = Column(String(50), nullable=True)
    purchase_price = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    loan_bank = Column(String(255), nullable=True)
    loan_amount = Column(Float, nullable=True)
    loan_left = Column(Float, nullable=True)
    insurance_company = Column(String(255), nullable=True)
    insurance_policy = Column(String(100), nullable=True)
    insurance_until = Column(Date, nullable=True)
    osago_until = Column(Date, nullable=True)
    last_maintenance = Column(Date, nullable=True)
    next_maintenance = Column(Date, nullable=True)
    maintenance_notes = Column(Text, nullable=True)
    condition = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="vehicles")
    
    __table_args__ = (
        Index("idx_vehicle_person_id", "person_id"),
        Index("idx_vehicle_vehicle_type", "vehicle_type"),
        Index("idx_vehicle_brand_model", "brand", "model"),
        Index("idx_vehicle_license_plate", "license_plate"),
        Index("idx_vehicle_is_active", "is_active"),
    )

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    case_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), default="medium")
    status = Column(String(20), default="active")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="cases")
    
    __table_args__ = (
        Index("idx_case_person_id", "person_id"),
        Index("idx_case_case_type", "case_type"),
        Index("idx_case_status", "status"),
        Index("idx_case_priority", "priority"),
    )

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    record_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    record_date = Column(DateTime, nullable=True)
    doctor_name = Column(String(255), nullable=True)
    attachments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="medical_records")
    
    __table_args__ = (
        Index("idx_medical_record_person_id", "person_id"),
        Index("idx_medical_record_record_type", "record_type"),
    )

class CrossRecord(Base):
    __tablename__ = "cross_records"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    record_type = Column(String(50), nullable=False)
    primary_category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    data = Column(JSON, nullable=True)
    record_date = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(20), default="active")
    importance = Column(Integer, default=0)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("persons.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", foreign_keys=[person_id], back_populates="cross_records")
    creator = relationship("Person", foreign_keys=[created_by], back_populates="cross_records_created")
    category = relationship("Category", back_populates="cross_records")
    
    __table_args__ = (
        Index("idx_cross_record_person_id", "person_id"),
        Index("idx_cross_record_record_type", "record_type"),
        Index("idx_cross_record_primary_category_id", "primary_category_id"),
        Index("idx_cross_record_status", "status"),
        Index("idx_cross_record_importance", "importance"),
        Index("idx_cross_record_record_date", "record_date"),
    )

class Relation(Base):
    __tablename__ = "relations"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    child_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    relation_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    parent = relationship("Person", foreign_keys=[parent_id], back_populates="relations_as_parent")
    child = relationship("Person", foreign_keys=[child_id], back_populates="relations_as_child")
    
    __table_args__ = (
        UniqueConstraint("parent_id", "child_id", name="uq_relation_parent_child"),
        Index("idx_relation_parent_id", "parent_id"),
        Index("idx_relation_child_id", "child_id"),
        Index("idx_relation_type", "relation_type"),
    )

class Partner(Base):
    __tablename__ = "partners"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    partner_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_type = Column(String(50), nullable=True)
    relationship_status = Column(String(50), nullable=True)
    relationship_label = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    breakup_reason = Column(Text, nullable=True)
    emotional_connection = Column(String(50), nullable=True)
    physical_connection = Column(String(50), nullable=True)
    relationship_rating = Column(Integer, nullable=True)
    relationship_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", foreign_keys=[person_id], back_populates="partners")
    partner_person = relationship("Person", foreign_keys=[partner_id], back_populates="partner_of")
    
    __table_args__ = (
        UniqueConstraint("person_id", "partner_id", name="uq_partner_person_partner"),
        Index("idx_partner_person_id", "person_id"),
        Index("idx_partner_partner_id", "partner_id"),
        Index("idx_partner_relationship_status", "relationship_status"),
        Index("idx_partner_relationship_type", "relationship_type"),
    )

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    device_type = Column(String(50), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    color = Column(String(50), nullable=True)
    specs = Column(Text, nullable=True)
    imei = Column(String(15), nullable=True)
    serial_number = Column(String(100), nullable=True)
    purchase_date = Column(Date, nullable=True)
    purchase_price = Column(Float, nullable=True)
    purchase_place = Column(String(255), nullable=True)
    warranty_until = Column(Date, nullable=True)
    accessories = Column(Text, nullable=True)
    condition = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="devices")
    
    __table_args__ = (
        Index("idx_device_person_id", "person_id"),
        Index("idx_device_device_type", "device_type"),
        Index("idx_device_brand_model", "brand", "model"),
        Index("idx_device_imei", "imei"),
        Index("idx_device_is_active", "is_active"),
    )

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(7), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    cross_records = relationship("CrossRecord", back_populates="category", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="category", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_category_name", "name"),
        Index("idx_category_slug", "slug"),
    )

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    category = relationship("Category", back_populates="tags")
    
    __table_args__ = (
        Index("idx_tag_name", "name"),
        Index("idx_tag_slug", "slug"),
        Index("idx_tag_category_id", "category_id"),
    )