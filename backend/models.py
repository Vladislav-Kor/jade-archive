from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    short_name = Column(String(100), nullable=False, unique=True)
    photo_path = Column(String(500), nullable=True)
    
    # Основная информация
    birth_date = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Параметры тела
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    clothing_size = Column(String(50), nullable=True)
    shoe_size = Column(Integer, nullable=True)
    chest_size = Column(Integer, nullable=True)
    waist_size = Column(Integer, nullable=True)
    hip_size = Column(Integer, nullable=True)
    
    # Медицинские данные
    blood_type = Column(String(10), nullable=True)
    rh_factor = Column(String(5), nullable=True)
    allergies = Column(Text, nullable=True)
    chronic_diseases = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    blood_pressure = Column(String(50), nullable=True)
    heart_rate = Column(Integer, nullable=True)
    
    # Документы
    passport_number = Column(String(50), nullable=True)
    inn = Column(String(50), nullable=True)
    snils = Column(String(50), nullable=True)
    driver_license_category = Column(String(50), nullable=True)
    driver_license_number = Column(String(50), nullable=True)
    
    # Социальные параметры
    marital_status = Column(String(50), nullable=True)
    children_count = Column(Integer, default=0)
    education = Column(String(255), nullable=True)
    profession = Column(String(255), nullable=True)
    workplace = Column(String(255), nullable=True)
    
    # Предпочтения
    favorite_color = Column(String(100), nullable=True)
    favorite_flowers = Column(String(255), nullable=True)
    favorite_food = Column(String(255), nullable=True)
    favorite_music = Column(String(255), nullable=True)
    favorite_movies = Column(String(255), nullable=True)
    hobbies = Column(Text, nullable=True)
    
    # Важность и заметки
    importance = Column(Float, default=0.0)
    importance_level = Column(String(20), default="medium")
    notes = Column(Text, nullable=True)
    
    # Системные поля
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    relations_as_parent = relationship("Relation", foreign_keys="Relation.parent_id", back_populates="parent")
    relations_as_child = relationship("Relation", foreign_keys="Relation.child_id", back_populates="child")
    social_media = relationship("SocialMedia", back_populates="person")
    tags_prefs = relationship("TagPreference", back_populates="person")

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