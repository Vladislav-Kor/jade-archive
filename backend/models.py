from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    short_name = Column(String(100), nullable=False, unique=True)
    photo_path = Column(String(500), nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
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
    favorite_flowers = Column(String(255), nullable=True)
    favorite_food = Column(String(255), nullable=True)
    favorite_music = Column(String(255), nullable=True)
    favorite_movies = Column(String(255), nullable=True)
    hobbies = Column(Text, nullable=True)
    importance = Column(Float, default=0.0)
    importance_level = Column(String(20), default="medium")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    relations_as_parent = relationship("Relation", foreign_keys="Relation.parent_id", back_populates="parent")
    relations_as_child = relationship("Relation", foreign_keys="Relation.child_id", back_populates="child")
    social_media = relationship("SocialMedia", back_populates="person")
    tags_prefs = relationship("TagPreference", back_populates="person")
    digital_accounts = relationship("DigitalAccount", back_populates="person", cascade="all, delete-orphan")

class Relation(Base):
    __tablename__ = "relations"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    child_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    relation_type = Column(String(100), nullable=False)
    
    parent = relationship("Person", foreign_keys=[parent_id], back_populates="relations_as_parent")
    child = relationship("Person", foreign_keys=[child_id], back_populates="relations_as_child")

class SocialMedia(Base):
    __tablename__ = "social_media"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    link = Column(String(500), nullable=False)
    
    person = relationship("Person", back_populates="social_media")

class TagPreference(Base):
    __tablename__ = "tags_and_prefs"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    category = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)
    
    person = relationship("Person", back_populates="tags_prefs")

class DigitalAccount(Base):
    __tablename__ = "digital_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    
    # Тип аккаунта
    platform_type = Column(String(50), nullable=False)
    platform_name = Column(String(100), nullable=False)
    
    # Данные аккаунта
    username = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    password = Column(Text, nullable=True)
    backup_codes = Column(Text, nullable=True)
    security_questions = Column(Text, nullable=True)
    
    # Игровые ID и идентификаторы
    account_id = Column(String(255), nullable=True)
    uid = Column(String(255), nullable=True)
    user_id = Column(String(255), nullable=True)
    friend_code = Column(String(255), nullable=True)
    server_id = Column(String(100), nullable=True)
    server_name = Column(String(255), nullable=True)
    region = Column(String(100), nullable=True)
    
    # Игровые данные
    nickname = Column(String(255), nullable=True)
    server = Column(String(100), nullable=True)
    level = Column(Integer, nullable=True)
    rank = Column(String(100), nullable=True)
    guild = Column(String(255), nullable=True)
    characters = Column(Text, nullable=True)
    
    # Дополнительная информация
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    person = relationship("Person", back_populates="digital_accounts")