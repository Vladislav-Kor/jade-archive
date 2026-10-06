# ============================================
# НОВЫЕ МОДЕЛИ ДЛЯ РАСШИРЕНИЯ ARC AGENT
# ============================================

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Date, Float, JSON, ARRAY, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Category(Base):
    """Категории разделов"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    icon = Column(String(50))
    color = Column(String(20))
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_system = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    children = relationship("Category", backref="parent", remote_side=[id])
    records = relationship("CrossRecord", back_populates="primary_category")

class Tag(Base):
    """Теги для записей"""
    __tablename__ = "record_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    color = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

class CrossRecord(Base):
    """Единая таблица записей"""
    __tablename__ = "cross_records"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    record_type = Column(String(50), nullable=False)
    
    primary_category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    secondary_categories = Column(ARRAY(Integer), default=[])
    
    data = Column(JSON)
    record_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    
    status = Column(String(20), default="active")
    importance = Column(Integer, default=0)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("persons.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    person = relationship("Person", foreign_keys=[person_id], back_populates="cross_records")
    creator = relationship("Person", foreign_keys=[created_by])
    primary_category = relationship("Category", back_populates="records")
    
    __table_args__ = (
        Index('idx_cross_records_person_id', 'person_id'),
        Index('idx_cross_records_category', 'primary_category_id'),
        Index('idx_cross_records_type', 'record_type'),
        Index('idx_cross_records_status', 'status'),
    )

class RecordTagRelation(Base):
    """Связь записей с тегами"""
    __tablename__ = "record_tag_relations"
    
    record_id = Column(Integer, ForeignKey("cross_records.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("record_tags.id"), primary_key=True)

class Partner(Base):
    """Партнеры и отношения"""
    __tablename__ = "partners"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    
    relationship_type = Column(String(50))
    relationship_status = Column(String(20))
    relationship_label = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    breakup_reason = Column(Text)
    
    emotional_connection = Column(String(20))
    physical_connection = Column(String(20))
    relationship_rating = Column(Integer)
    relationship_notes = Column(Text)
    
    sex_quality = Column(String(20))
    sex_frequency = Column(String(30))
    sex_rating = Column(Integer)
    sex_protection = Column(Boolean)
    sex_positions_used = Column(JSON)
    sex_special = Column(Text)
    sex_fetishes_shared = Column(JSON)
    sex_chemistry = Column(String(20))
    sex_compatibility = Column(String(20))
    sex_first_date = Column(Date)
    sex_last_date = Column(Date)
    sex_count = Column(Integer)
    
    intimacy_level = Column(String(20))
    trust_level = Column(String(20))
    vulnerability = Column(String(20))
    communication_style = Column(String(20))
    conflict_resolution = Column(String(20))
    shared_values = Column(Text)
    shared_goals = Column(Text)
    relationship_challenges = Column(Text)
    relationship_growth = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    person = relationship("Person", foreign_keys=[person_id], back_populates="partners")
    partner = relationship("Person", foreign_keys=[partner_id])
    
    __table_args__ = (
        Index('idx_partners_person_id', 'person_id'),
        Index('idx_partners_partner_id', 'partner_id'),
    )

class Device(Base):
    """Техника"""
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    
    device_type = Column(String(50), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    color = Column(String(50))
    specs = Column(Text)
    imei = Column(String(50))
    serial_number = Column(String(50))
    purchase_date = Column(Date)
    purchase_price = Column(Float)
    purchase_place = Column(String(255))
    warranty_until = Column(Date)
    accessories = Column(Text)
    condition = Column(String(30))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    person = relationship("Person", back_populates="devices")
    
    __table_args__ = (
        Index('idx_devices_person_id', 'person_id'),
        Index('idx_devices_type', 'device_type'),
    )

class Audit(Base):
    """Аудит изменений"""
    __tablename__ = "audit"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    changed_by = Column(Integer, ForeignKey("persons.id"), nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)
    field_name = Column(String(100))
    old_value = Column(Text)
    new_value = Column(Text)
    change_reason = Column(Text)
    viewed_by = Column(Integer, ForeignKey("persons.id"), nullable=True)
    viewed_at = Column(DateTime)
    
    # Relationships
    person = relationship("Person", foreign_keys=[person_id])
    changer = relationship("Person", foreign_keys=[changed_by])
    viewer = relationship("Person", foreign_keys=[viewed_by])
    
    __table_args__ = (
        Index('idx_audit_person_id', 'person_id'),
        Index('idx_audit_changed_at', 'changed_at'),
    )
