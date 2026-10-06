"""
crud.py - Complete CRUD operations for Jade Archive API
Production-ready with full error handling and validation
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional, Any
from datetime import datetime, date
import logging
import json

import models
import schemas

logger = logging.getLogger(__name__)

# ============================================
# PERSON CRUD
# ============================================

def get_person(db: Session, person_id: int) -> Optional[models.Person]:
    try:
        return db.query(models.Person).filter(models.Person.id == person_id).first()
    except Exception as e:
        logger.error(f"Error getting person {person_id}: {e}")
        raise

def get_person_by_short_name(db: Session, short_name: str) -> Optional[models.Person]:
    try:
        return db.query(models.Person).filter(
            models.Person.short_name == short_name
        ).first()
    except Exception as e:
        logger.error(f"Error getting person by short name {short_name}: {e}")
        raise

def get_persons(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[models.Person]:
    try:
        query = db.query(models.Person)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    models.Person.full_name.ilike(search_term),
                    models.Person.short_name.ilike(search_term),
                    models.Person.email.ilike(search_term),
                    models.Person.phone.ilike(search_term)
                )
            )
        
        return query.order_by(models.Person.full_name).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting persons: {e}")
        raise

def create_person(db: Session, person: schemas.PersonCreate) -> models.Person:
    try:
        db_person = models.Person(
            full_name=person.full_name.strip(),
            short_name=person.short_name.strip(),
            photo_path=person.photo_path,
            birth_date=person.birth_date,
            gender=person.gender,
            address=person.address,
            phone=person.phone,
            email=person.email,
            height=person.height,
            weight=person.weight,
            clothing_size=person.clothing_size,
            shoe_size=person.shoe_size,
            chest_size=person.chest_size,
            waist_size=person.waist_size,
            hip_size=person.hip_size,
            blood_type=person.blood_type,
            rh_factor=person.rh_factor,
            allergies=person.allergies,
            chronic_diseases=person.chronic_diseases,
            medications=person.medications,
            blood_pressure=person.blood_pressure,
            heart_rate=person.heart_rate,
            passport_number=person.passport_number,
            inn=person.inn,
            snils=person.snils,
            driver_license_category=person.driver_license_category,
            driver_license_number=person.driver_license_number,
            marital_status=person.marital_status,
            children_count=person.children_count or 0,
            education=person.education,
            profession=person.profession,
            workplace=person.workplace,
            favorite_color=person.favorite_color,
            favorite_flowers=person.favorite_flowers,
            favorite_food=person.favorite_food,
            favorite_music=person.favorite_music,
            favorite_movies=person.favorite_movies,
            hobbies=person.hobbies,
            importance=person.importance or 0.0,
            importance_level=person.importance_level or "medium",
            notes=person.notes
        )
        
        db.add(db_person)
        db.commit()
        db.refresh(db_person)
        return db_person
    except Exception as e:
        logger.error(f"Error creating person: {e}")
        db.rollback()
        raise

def update_person(
    db: Session,
    person_id: int,
    person_update: schemas.PersonUpdate
) -> Optional[models.Person]:
    try:
        db_person = get_person(db, person_id)
        if not db_person:
            return None
        
        update_data = person_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_person, key, value)
        
        db_person.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_person)
        return db_person
    except Exception as e:
        logger.error(f"Error updating person {person_id}: {e}")
        db.rollback()
        raise

def delete_person(db: Session, person_id: int) -> bool:
    try:
        db_person = get_person(db, person_id)
        if not db_person:
            return False
        
        db.query(models.Relation).filter(
            or_(
                models.Relation.parent_id == person_id,
                models.Relation.child_id == person_id
            )
        ).delete()
        
        db.query(models.SocialMedia).filter(models.SocialMedia.person_id == person_id).delete()
        db.query(models.TagPreference).filter(models.TagPreference.person_id == person_id).delete()
        db.query(models.DigitalAccount).filter(models.DigitalAccount.person_id == person_id).delete()
        db.query(models.RealEstate).filter(models.RealEstate.person_id == person_id).delete()
        db.query(models.Vehicle).filter(models.Vehicle.person_id == person_id).delete()
        db.query(models.Case).filter(models.Case.person_id == person_id).delete()
        db.query(models.MedicalRecord).filter(models.MedicalRecord.person_id == person_id).delete()
        db.query(models.CrossRecord).filter(models.CrossRecord.person_id == person_id).delete()
        db.query(models.Partner).filter(
            or_(
                models.Partner.person_id == person_id,
                models.Partner.partner_id == person_id
            )
        ).delete()
        db.query(models.Device).filter(models.Device.person_id == person_id).delete()
        
        db.delete(db_person)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting person {person_id}: {e}")
        db.rollback()
        raise

def search_persons(db: Session, query: str, limit: int = 20) -> List[models.Person]:
    try:
        search_term = f"%{query}%"
        return db.query(models.Person).filter(
            or_(
                models.Person.full_name.ilike(search_term),
                models.Person.short_name.ilike(search_term),
                models.Person.email.ilike(search_term),
                models.Person.phone.ilike(search_term)
            )
        ).limit(limit).all()
    except Exception as e:
        logger.error(f"Error searching persons: {e}")
        raise

# ============================================
# RELATION CRUD
# ============================================

def get_relations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Relation]:
    try:
        return db.query(models.Relation).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting relations: {e}")
        raise

def get_person_relations(db: Session, person_id: int) -> List[dict]:
    try:
        relations_as_parent = db.query(models.Relation).filter(
            models.Relation.parent_id == person_id
        ).all()
        
        relations_as_child = db.query(models.Relation).filter(
            models.Relation.child_id == person_id
        ).all()
        
        result = []
        
        for rel in relations_as_parent:
            child = get_person(db, rel.child_id)
            result.append({
                "id": rel.id,
                "parent_id": rel.parent_id,
                "child_id": rel.child_id,
                "relation_type": rel.relation_type,
                "direction": "outgoing",
                "person_name": child.full_name if child else "Unknown",
                "person_id": rel.child_id,
                "created_at": rel.created_at,
                "updated_at": rel.updated_at
            })
        
        for rel in relations_as_child:
            parent = get_person(db, rel.parent_id)
            result.append({
                "id": rel.id,
                "parent_id": rel.parent_id,
                "child_id": rel.child_id,
                "relation_type": rel.relation_type,
                "direction": "incoming",
                "person_name": parent.full_name if parent else "Unknown",
                "person_id": rel.parent_id,
                "created_at": rel.created_at,
                "updated_at": rel.updated_at
            })
        
        return result
    except Exception as e:
        logger.error(f"Error getting person relations for {person_id}: {e}")
        raise

def create_relation(db: Session, relation: schemas.RelationCreate) -> models.Relation:
    try:
        db_relation = models.Relation(
            parent_id=relation.parent_id,
            child_id=relation.child_id,
            relation_type=relation.relation_type.strip()
        )
        
        db.add(db_relation)
        db.commit()
        db.refresh(db_relation)
        return db_relation
    except Exception as e:
        logger.error(f"Error creating relation: {e}")
        db.rollback()
        raise

def delete_relation(db: Session, relation_id: int) -> bool:
    try:
        db_relation = db.query(models.Relation).filter(
            models.Relation.id == relation_id
        ).first()
        
        if not db_relation:
            return False
        
        db.delete(db_relation)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting relation {relation_id}: {e}")
        db.rollback()
        raise

# ============================================
# SOCIAL MEDIA CRUD
# ============================================

def get_social_media(db: Session, person_id: int) -> List[models.SocialMedia]:
    try:
        return db.query(models.SocialMedia).filter(
            models.SocialMedia.person_id == person_id
        ).all()
    except Exception as e:
        logger.error(f"Error getting social media for person {person_id}: {e}")
        raise

def add_social_media(
    db: Session,
    person_id: int,
    social: schemas.SocialMediaBase
) -> models.SocialMedia:
    try:
        db_social = models.SocialMedia(
            person_id=person_id,
            platform=social.platform.strip(),
            link=social.link.strip()
        )
        
        db.add(db_social)
        db.commit()
        db.refresh(db_social)
        return db_social
    except Exception as e:
        logger.error(f"Error adding social media: {e}")
        db.rollback()
        raise

def update_social_media(
    db: Session,
    social_id: int,
    social: schemas.SocialMediaBase
) -> Optional[models.SocialMedia]:
    try:
        db_social = db.query(models.SocialMedia).filter(
            models.SocialMedia.id == social_id
        ).first()
        if not db_social:
            return None

        db_social.platform = social.platform.strip()
        db_social.link = social.link.strip()
        db.commit()
        db.refresh(db_social)
        return db_social
    except Exception as e:
        logger.error(f"Error updating social media {social_id}: {e}")
        db.rollback()
        raise

def delete_social_media(db: Session, social_id: int) -> bool:
    try:
        db_social = db.query(models.SocialMedia).filter(
            models.SocialMedia.id == social_id
        ).first()
        
        if not db_social:
            return False
        
        db.delete(db_social)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting social media {social_id}: {e}")
        db.rollback()
        raise

# ============================================
# TAG PREFERENCES CRUD
# ============================================

def get_tags(db: Session, person_id: int) -> List[models.TagPreference]:
    try:
        return db.query(models.TagPreference).filter(
            models.TagPreference.person_id == person_id
        ).all()
    except Exception as e:
        logger.error(f"Error getting tags for person {person_id}: {e}")
        raise

def add_tag(
    db: Session,
    person_id: int,
    tag: schemas.TagPreferenceBase
) -> models.TagPreference:
    try:
        db_tag = models.TagPreference(
            person_id=person_id,
            category=tag.category.strip(),
            value=tag.value.strip()
        )
        
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except Exception as e:
        logger.error(f"Error adding tag: {e}")
        db.rollback()
        raise

def delete_tag(db: Session, tag_id: int) -> bool:
    try:
        db_tag = db.query(models.TagPreference).filter(
            models.TagPreference.id == tag_id
        ).first()
        
        if not db_tag:
            return False
        
        db.delete(db_tag)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting tag {tag_id}: {e}")
        db.rollback()
        raise

# ============================================
# DIGITAL ACCOUNT CRUD
# ============================================

def get_digital_accounts(db: Session, person_id: int) -> List[models.DigitalAccount]:
    try:
        return db.query(models.DigitalAccount).filter(
            models.DigitalAccount.person_id == person_id,
            models.DigitalAccount.is_active == True
        ).all()
    except Exception as e:
        logger.error(f"Error getting digital accounts for person {person_id}: {e}")
        raise

def get_digital_account(db: Session, account_id: int) -> Optional[models.DigitalAccount]:
    try:
        return db.query(models.DigitalAccount).filter(
            models.DigitalAccount.id == account_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting digital account {account_id}: {e}")
        raise

def create_digital_account(
    db: Session,
    person_id: int,
    account: schemas.DigitalAccountCreate
) -> models.DigitalAccount:
    try:
        db_account = models.DigitalAccount(
            person_id=person_id,
            platform_type=account.platform_type.strip(),
            platform_name=account.platform_name.strip(),
            username=account.username,
            email=account.email,
            phone=account.phone,
            password=account.password,
            backup_codes=account.backup_codes,
            security_questions=account.security_questions,
            account_id=account.account_id,
            uid=account.uid,
            user_id=account.user_id,
            friend_code=account.friend_code,
            server_id=account.server_id,
            server_name=account.server_name,
            region=account.region,
            nickname=account.nickname,
            server=account.server,
            level=account.level,
            rank=account.rank,
            guild=account.guild,
            characters=account.characters,
            notes=account.notes,
            is_active=account.is_active if account.is_active is not None else True
        )
        
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as e:
        logger.error(f"Error creating digital account: {e}")
        db.rollback()
        raise

def update_digital_account(
    db: Session,
    account_id: int,
    account_update: schemas.DigitalAccountUpdate
) -> Optional[models.DigitalAccount]:
    try:
        db_account = get_digital_account(db, account_id)
        if not db_account:
            return None
        
        update_data = account_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_account, key, value)
        
        db_account.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as e:
        logger.error(f"Error updating digital account {account_id}: {e}")
        db.rollback()
        raise

def delete_digital_account(db: Session, account_id: int) -> bool:
    try:
        db_account = get_digital_account(db, account_id)
        if not db_account:
            return False
        
        db_account.is_active = False
        db_account.updated_at = datetime.utcnow()
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting digital account {account_id}: {e}")
        db.rollback()
        raise

# ============================================
# REAL ESTATE CRUD
# ============================================

def get_real_estate(db: Session, person_id: int) -> List[models.RealEstate]:
    try:
        return db.query(models.RealEstate).filter(
            models.RealEstate.person_id == person_id,
            models.RealEstate.is_active == True
        ).all()
    except Exception as e:
        logger.error(f"Error getting real estate for person {person_id}: {e}")
        raise

def get_real_estate_item(db: Session, property_id: int) -> Optional[models.RealEstate]:
    try:
        return db.query(models.RealEstate).filter(
            models.RealEstate.id == property_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting real estate item {property_id}: {e}")
        raise

def create_real_estate(
    db: Session,
    person_id: int,
    property_data: schemas.RealEstateCreate
) -> models.RealEstate:
    try:
        db_property = models.RealEstate(
            person_id=person_id,
            property_type=property_data.property_type.strip(),
            property_name=property_data.property_name.strip() if property_data.property_name else None,
            address=property_data.address.strip(),
            total_area=property_data.total_area,
            living_area=property_data.living_area,
            land_area=property_data.land_area,
            floor=property_data.floor,
            total_floors=property_data.total_floors,
            rooms_count=property_data.rooms_count,
            bathroom_count=property_data.bathroom_count,
            balcony_count=property_data.balcony_count,
            ownership_type=property_data.ownership_type,
            ownership_percent=property_data.ownership_percent or 100.0,
            cadastral_number=property_data.cadastral_number,
            registration_date=property_data.registration_date,
            purchase_price=property_data.purchase_price,
            current_value=property_data.current_value,
            mortgage_bank=property_data.mortgage_bank,
            mortgage_amount=property_data.mortgage_amount,
            mortgage_left=property_data.mortgage_left,
            condition=property_data.condition,
            year_built=property_data.year_built,
            renovation_year=property_data.renovation_year,
            notes=property_data.notes,
            is_active=property_data.is_active
        )
        
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        return db_property
    except Exception as e:
        logger.error(f"Error creating real estate: {e}")
        db.rollback()
        raise

def update_real_estate(
    db: Session,
    property_id: int,
    property_update: schemas.RealEstateUpdate
) -> Optional[models.RealEstate]:
    try:
        db_property = get_real_estate_item(db, property_id)
        if not db_property:
            return None
        
        update_data = property_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_property, key, value)
        
        db_property.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_property)
        return db_property
    except Exception as e:
        logger.error(f"Error updating real estate {property_id}: {e}")
        db.rollback()
        raise

def delete_real_estate(db: Session, property_id: int) -> bool:
    try:
        db_property = get_real_estate_item(db, property_id)
        if not db_property:
            return False
        
        db_property.is_active = False
        db_property.updated_at = datetime.utcnow()
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting real estate {property_id}: {e}")
        db.rollback()
        raise

# ============================================
# VEHICLE CRUD
# ============================================

def get_vehicles(db: Session, person_id: int) -> List[models.Vehicle]:
    try:
        return db.query(models.Vehicle).filter(
            models.Vehicle.person_id == person_id,
            models.Vehicle.is_active == True
        ).all()
    except Exception as e:
        logger.error(f"Error getting vehicles for person {person_id}: {e}")
        raise

def get_vehicle(db: Session, vehicle_id: int) -> Optional[models.Vehicle]:
    try:
        return db.query(models.Vehicle).filter(
            models.Vehicle.id == vehicle_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting vehicle {vehicle_id}: {e}")
        raise

def create_vehicle(
    db: Session,
    person_id: int,
    vehicle_data: schemas.VehicleCreate
) -> models.Vehicle:
    try:
        db_vehicle = models.Vehicle(
            person_id=person_id,
            vehicle_type=vehicle_data.vehicle_type.strip(),
            brand=vehicle_data.brand.strip(),
            model=vehicle_data.model.strip(),
            year=vehicle_data.year,
            color=vehicle_data.color,
            license_plate=vehicle_data.license_plate,
            vin=vehicle_data.vin,
            engine_number=vehicle_data.engine_number,
            chassis_number=vehicle_data.chassis_number,
            engine_capacity=vehicle_data.engine_capacity,
            horsepower=vehicle_data.horsepower,
            mileage=vehicle_data.mileage,
            transmission=vehicle_data.transmission,
            drive_type=vehicle_data.drive_type,
            fuel_type=vehicle_data.fuel_type,
            ownership_type=vehicle_data.ownership_type,
            registration_date=vehicle_data.registration_date,
            registration_number=vehicle_data.registration_number,
            purchase_price=vehicle_data.purchase_price,
            current_value=vehicle_data.current_value,
            loan_bank=vehicle_data.loan_bank,
            loan_amount=vehicle_data.loan_amount,
            loan_left=vehicle_data.loan_left,
            insurance_company=vehicle_data.insurance_company,
            insurance_policy=vehicle_data.insurance_policy,
            insurance_until=vehicle_data.insurance_until,
            osago_until=vehicle_data.osago_until,
            last_maintenance=vehicle_data.last_maintenance,
            next_maintenance=vehicle_data.next_maintenance,
            maintenance_notes=vehicle_data.maintenance_notes,
            condition=vehicle_data.condition,
            notes=vehicle_data.notes,
            is_active=vehicle_data.is_active
        )
        
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    except Exception as e:
        logger.error(f"Error creating vehicle: {e}")
        db.rollback()
        raise

def update_vehicle(
    db: Session,
    vehicle_id: int,
    vehicle_update: schemas.VehicleUpdate
) -> Optional[models.Vehicle]:
    try:
        db_vehicle = get_vehicle(db, vehicle_id)
        if not db_vehicle:
            return None
        
        update_data = vehicle_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_vehicle, key, value)
        
        db_vehicle.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    except Exception as e:
        logger.error(f"Error updating vehicle {vehicle_id}: {e}")
        db.rollback()
        raise

def delete_vehicle(db: Session, vehicle_id: int) -> bool:
    try:
        db_vehicle = get_vehicle(db, vehicle_id)
        if not db_vehicle:
            return False
        
        db_vehicle.is_active = False
        db_vehicle.updated_at = datetime.utcnow()
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting vehicle {vehicle_id}: {e}")
        db.rollback()
        raise

# ============================================
# CASE CRUD
# ============================================

def get_cases(db: Session, person_id: int) -> List[models.Case]:
    try:
        return db.query(models.Case).filter(
            models.Case.person_id == person_id
        ).all()
    except Exception as e:
        logger.error(f"Error getting cases for person {person_id}: {e}")
        raise

def get_case(db: Session, case_id: int) -> Optional[models.Case]:
    try:
        return db.query(models.Case).filter(
            models.Case.id == case_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting case {case_id}: {e}")
        raise

def create_case(
    db: Session,
    person_id: int,
    case_data: schemas.CaseCreate
) -> models.Case:
    try:
        db_case = models.Case(
            person_id=person_id,
            case_type=case_data.case_type.strip(),
            title=case_data.title.strip(),
            description=case_data.description,
            priority=case_data.priority or "medium",
            status=case_data.status or "active",
            due_date=case_data.due_date
        )
        
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
        return db_case
    except Exception as e:
        logger.error(f"Error creating case: {e}")
        db.rollback()
        raise

def update_case(
    db: Session,
    case_id: int,
    case_update: schemas.CaseUpdate
) -> Optional[models.Case]:
    try:
        db_case = get_case(db, case_id)
        if not db_case:
            return None
        
        update_data = case_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_case, key, value)
        
        db_case.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_case)
        return db_case
    except Exception as e:
        logger.error(f"Error updating case {case_id}: {e}")
        db.rollback()
        raise

def delete_case(db: Session, case_id: int) -> bool:
    try:
        db_case = get_case(db, case_id)
        if not db_case:
            return False
        
        db.delete(db_case)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting case {case_id}: {e}")
        db.rollback()
        raise

# ============================================
# MEDICAL RECORD CRUD
# ============================================

def get_medical_records(db: Session, person_id: int) -> List[models.MedicalRecord]:
    try:
        return db.query(models.MedicalRecord).filter(
            models.MedicalRecord.person_id == person_id
        ).all()
    except Exception as e:
        logger.error(f"Error getting medical records for person {person_id}: {e}")
        raise

def get_medical_record(db: Session, record_id: int) -> Optional[models.MedicalRecord]:
    try:
        return db.query(models.MedicalRecord).filter(
            models.MedicalRecord.id == record_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting medical record {record_id}: {e}")
        raise

def create_medical_record(
    db: Session,
    person_id: int,
    record_data: schemas.MedicalRecordCreate
) -> models.MedicalRecord:
    try:
        db_record = models.MedicalRecord(
            person_id=person_id,
            record_type=record_data.record_type.strip(),
            title=record_data.title.strip(),
            description=record_data.description,
            record_date=record_data.record_date,
            doctor_name=record_data.doctor_name,
            attachments=record_data.attachments
        )
        
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    except Exception as e:
        logger.error(f"Error creating medical record: {e}")
        db.rollback()
        raise

def update_medical_record(
    db: Session,
    record_id: int,
    record_update: schemas.MedicalRecordUpdate
) -> Optional[models.MedicalRecord]:
    try:
        db_record = get_medical_record(db, record_id)
        if not db_record:
            return None
        
        update_data = record_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_record, key, value)
        
        db_record.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_record)
        return db_record
    except Exception as e:
        logger.error(f"Error updating medical record {record_id}: {e}")
        db.rollback()
        raise

def delete_medical_record(db: Session, record_id: int) -> bool:
    try:
        db_record = get_medical_record(db, record_id)
        if not db_record:
            return False
        
        db.delete(db_record)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting medical record {record_id}: {e}")
        db.rollback()
        raise

# ============================================
# PARTNER CRUD
# ============================================

def get_partners(db: Session, person_id: int) -> List[models.Partner]:
    try:
        return db.query(models.Partner).filter(
            models.Partner.person_id == person_id
        ).all()
    except Exception as e:
        logger.error(f"Error getting partners for person {person_id}: {e}")
        raise

def get_partner(db: Session, partner_id: int) -> Optional[models.Partner]:
    try:
        return db.query(models.Partner).filter(
            models.Partner.id == partner_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting partner {partner_id}: {e}")
        raise

def create_partner(
    db: Session,
    partner_data: schemas.PartnerCreate
) -> models.Partner:
    try:
        db_partner = models.Partner(
            person_id=partner_data.person_id,
            partner_id=partner_data.partner_id,
            relationship_type=partner_data.relationship_type,
            relationship_status=partner_data.relationship_status,
            relationship_label=partner_data.relationship_label,
            start_date=partner_data.start_date,
            end_date=partner_data.end_date,
            breakup_reason=partner_data.breakup_reason,
            emotional_connection=partner_data.emotional_connection,
            physical_connection=partner_data.physical_connection,
            relationship_rating=partner_data.relationship_rating,
            relationship_notes=partner_data.relationship_notes
        )
        
        db.add(db_partner)
        db.commit()
        db.refresh(db_partner)
        return db_partner
    except Exception as e:
        logger.error(f"Error creating partner: {e}")
        db.rollback()
        raise

def update_partner(
    db: Session,
    partner_id: int,
    partner_update: schemas.PartnerUpdate
) -> Optional[models.Partner]:
    try:
        db_partner = get_partner(db, partner_id)
        if not db_partner:
            return None
        
        update_data = partner_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_partner, key, value)
        
        db_partner.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_partner)
        return db_partner
    except Exception as e:
        logger.error(f"Error updating partner {partner_id}: {e}")
        db.rollback()
        raise

def delete_partner(db: Session, partner_id: int) -> bool:
    try:
        db_partner = get_partner(db, partner_id)
        if not db_partner:
            return False
        
        db.delete(db_partner)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting partner {partner_id}: {e}")
        db.rollback()
        raise

# ============================================
# DEVICE CRUD
# ============================================

def get_devices(db: Session, person_id: int) -> List[models.Device]:
    try:
        return db.query(models.Device).filter(
            models.Device.person_id == person_id,
            models.Device.is_active == True
        ).all()
    except Exception as e:
        logger.error(f"Error getting devices for person {person_id}: {e}")
        raise

def get_device(db: Session, device_id: int) -> Optional[models.Device]:
    try:
        return db.query(models.Device).filter(
            models.Device.id == device_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting device {device_id}: {e}")
        raise

def create_device(
    db: Session,
    device_data: schemas.DeviceCreate
) -> models.Device:
    try:
        db_device = models.Device(
            person_id=device_data.person_id,
            device_type=device_data.device_type.strip(),
            brand=device_data.brand.strip(),
            model=device_data.model.strip(),
            color=device_data.color,
            specs=device_data.specs,
            imei=device_data.imei,
            serial_number=device_data.serial_number,
            purchase_date=device_data.purchase_date,
            purchase_price=device_data.purchase_price,
            purchase_place=device_data.purchase_place,
            warranty_until=device_data.warranty_until,
            accessories=device_data.accessories,
            condition=device_data.condition,
            notes=device_data.notes,
            is_active=device_data.is_active
        )
        
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        db.rollback()
        raise

def update_device(
    db: Session,
    device_id: int,
    device_update: schemas.DeviceUpdate
) -> Optional[models.Device]:
    try:
        db_device = get_device(db, device_id)
        if not db_device:
            return None
        
        update_data = device_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_device, key, value)
        
        db_device.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_device)
        return db_device
    except Exception as e:
        logger.error(f"Error updating device {device_id}: {e}")
        db.rollback()
        raise

def delete_device(db: Session, device_id: int) -> bool:
    try:
        db_device = get_device(db, device_id)
        if not db_device:
            return False
        
        db_device.is_active = False
        db_device.updated_at = datetime.utcnow()
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting device {device_id}: {e}")
        db.rollback()
        raise

# ============================================
# CROSS RECORD CRUD
# ============================================

def get_cross_records(db: Session, person_id: int) -> List[models.CrossRecord]:
    try:
        return db.query(models.CrossRecord).filter(
            models.CrossRecord.person_id == person_id
        ).all()
    except Exception as e:
        logger.error(f"Error getting cross records for person {person_id}: {e}")
        raise

def get_cross_record(db: Session, record_id: int) -> Optional[models.CrossRecord]:
    try:
        return db.query(models.CrossRecord).filter(
            models.CrossRecord.id == record_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting cross record {record_id}: {e}")
        raise

def create_cross_record(
    db: Session,
    record_data: schemas.CrossRecordCreate
) -> models.CrossRecord:
    try:
        db_record = models.CrossRecord(
            person_id=record_data.person_id,
            title=record_data.title.strip(),
            description=record_data.description,
            record_type=record_data.record_type.strip(),
            primary_category_id=record_data.primary_category_id,
            data=record_data.data,
            record_date=record_data.record_date,
            start_date=record_data.start_date,
            end_date=record_data.end_date,
            status=record_data.status or "active",
            importance=record_data.importance or 0,
            is_private=record_data.is_private or False,
            created_by=record_data.created_by
        )
        
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    except Exception as e:
        logger.error(f"Error creating cross record: {e}")
        db.rollback()
        raise

def update_cross_record(
    db: Session,
    record_id: int,
    record_update: schemas.CrossRecordUpdate
) -> Optional[models.CrossRecord]:
    try:
        db_record = get_cross_record(db, record_id)
        if not db_record:
            return None
        
        update_data = record_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_record, key, value)
        
        db_record.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_record)
        return db_record
    except Exception as e:
        logger.error(f"Error updating cross record {record_id}: {e}")
        db.rollback()
        raise

def delete_cross_record(db: Session, record_id: int) -> bool:
    try:
        db_record = get_cross_record(db, record_id)
        if not db_record:
            return False
        
        db.delete(db_record)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting cross record {record_id}: {e}")
        db.rollback()
        raise

# ============================================
# CATEGORY CRUD
# ============================================

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    try:
        return db.query(models.Category).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    try:
        return db.query(models.Category).filter(
            models.Category.id == category_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting category {category_id}: {e}")
        raise

def create_category(db: Session, category_data: schemas.CategoryCreate) -> models.Category:
    try:
        db_category = models.Category(
            name=category_data.name.strip(),
            slug=category_data.slug.strip(),
            icon=category_data.icon,
            color=category_data.color,
            description=category_data.description
        )
        
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        db.rollback()
        raise

def update_category(
    db: Session,
    category_id: int,
    category_update: schemas.CategoryUpdate
) -> Optional[models.Category]:
    try:
        db_category = get_category(db, category_id)
        if not db_category:
            return None
        
        update_data = category_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_category, key, value)
        
        db_category.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        logger.error(f"Error updating category {category_id}: {e}")
        db.rollback()
        raise

def delete_category(db: Session, category_id: int) -> bool:
    try:
        db_category = get_category(db, category_id)
        if not db_category:
            return False
        
        db.delete(db_category)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting category {category_id}: {e}")
        db.rollback()
        raise

# ============================================
# TAG CRUD
# ============================================

def get_tags_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.Tag]:
    try:
        return db.query(models.Tag).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting tags: {e}")
        raise

def get_tag(db: Session, tag_id: int) -> Optional[models.Tag]:
    try:
        return db.query(models.Tag).filter(
            models.Tag.id == tag_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting tag {tag_id}: {e}")
        raise

def create_tag(db: Session, tag_data: schemas.TagCreate) -> models.Tag:
    try:
        db_tag = models.Tag(
            name=tag_data.name.strip(),
            slug=tag_data.slug.strip(),
            category_id=tag_data.category_id,
            description=tag_data.description,
            color=tag_data.color
        )
        
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except Exception as e:
        logger.error(f"Error creating tag: {e}")
        db.rollback()
        raise

def update_tag(
    db: Session,
    tag_id: int,
    tag_update: schemas.TagUpdate
) -> Optional[models.Tag]:
    try:
        db_tag = get_tag(db, tag_id)
        if not db_tag:
            return None
        
        update_data = tag_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, str) and value:
                value = value.strip()
            setattr(db_tag, key, value)
        
        db_tag.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except Exception as e:
        logger.error(f"Error updating tag {tag_id}: {e}")
        db.rollback()
        raise

def delete_tag(db: Session, tag_id: int) -> bool:
    try:
        db_tag = get_tag(db, tag_id)
        if not db_tag:
            return False
        
        db.delete(db_tag)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting tag {tag_id}: {e}")
        db.rollback()
        raise

# ============================================
# TREE BUILDING
# ============================================

def build_tree(
    db: Session,
    root_id: int,
    max_depth: int = 10,
    current_depth: int = 0
) -> Optional[schemas.TreeNode]:
    try:
        if current_depth > max_depth:
            return None
        
        root = get_person(db, root_id)
        if not root:
            return None
        
        children_relations = db.query(models.Relation).filter(
            models.Relation.parent_id == root_id
        ).all()
        
        children = []
        for rel in children_relations:
            child_node = build_tree(db, rel.child_id, max_depth, current_depth + 1)
            if child_node:
                children.append(child_node)
        
        return schemas.TreeNode(
            id=root.id,
            name=root.full_name,
            short_name=root.short_name,
            importance=root.importance or 0.0,
            importance_level=root.importance_level or "medium",
            children=children
        )
    except Exception as e:
        logger.error(f"Error building tree from root {root_id}: {e}")
        raise

# ============================================
# BULK OPERATIONS
# ============================================

def bulk_create_persons(
    db: Session,
    persons: List[schemas.PersonCreate]
) -> List[models.Person]:
    try:
        results = []
        for person_data in persons:
            db_person = create_person(db, person_data)
            results.append(db_person)
        return results
    except Exception as e:
        logger.error(f"Error in bulk create persons: {e}")
        db.rollback()
        raise