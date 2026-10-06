# ============================================
# CRUD ОПЕРАЦИИ ДЛЯ НОВЫХ МОДЕЛЕЙ
# ============================================

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime
import models, schemas, models_extension

# ============================================
# CRUD для Категорий
# ============================================

def get_category(db: Session, category_id: int):
    return db.query(models_extension.Category).filter(models_extension.Category.id == category_id).first()

def get_category_by_slug(db: Session, slug: str):
    return db.query(models_extension.Category).filter(models_extension.Category.slug == slug).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_extension.Category).order_by(models_extension.Category.sort_order).offset(skip).limit(limit).all()

def create_category(db: Session, category_data):
    db_category = models_extension.Category(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_data):
    db_category = get_category(db, category_id)
    if db_category:
        for key, value in category_data.model_dump().items():
            if value is not None:
                setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category and not db_category.is_system:
        db.delete(db_category)
        db.commit()
        return True
    return False

# ============================================
# CRUD для Кросс-записей
# ============================================

def get_cross_records(db: Session, person_id: int, category_id: int = None, record_type: str = None):
    query = db.query(models_extension.CrossRecord).filter(models_extension.CrossRecord.person_id == person_id)
    
    if category_id:
        query = query.filter(
            or_(
                models_extension.CrossRecord.primary_category_id == category_id,
                models_extension.CrossRecord.secondary_categories.any(category_id)
            )
        )
    
    if record_type:
        query = query.filter(models_extension.CrossRecord.record_type == record_type)
    
    return query.order_by(desc(models_extension.CrossRecord.created_at)).all()

def get_cross_record(db: Session, record_id: int):
    return db.query(models_extension.CrossRecord).filter(models_extension.CrossRecord.id == record_id).first()

def create_cross_record(db: Session, person_id: int, record_data, created_by: int = None):
    # Автоматическое добавление категорий
    secondary_categories = list(record_data.secondary_categories) if record_data.secondary_categories else []
    
    # Если тип записи - disease (болезнь) и категория Интимное здоровье (3)
    if record_data.record_type == 'disease' and record_data.primary_category_id == 3:
        # Добавляем Медицина (1) и Секс (2)
        if 1 not in secondary_categories:
            secondary_categories.append(1)
        if 2 not in secondary_categories:
            secondary_categories.append(2)
    
    # Если тип записи - medication (препарат)
    if record_data.record_type == 'medication':
        # Добавляем Медицина (1)
        if 1 not in secondary_categories:
            secondary_categories.append(1)
    
    # Создаем запись
    db_record = models_extension.CrossRecord(
        person_id=person_id,
        created_by=created_by,
        secondary_categories=secondary_categories,
        **record_data.model_dump(exclude={'secondary_categories'})
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_cross_record(db: Session, record_id: int, record_data):
    db_record = get_cross_record(db, record_id)
    if db_record:
        update_data = record_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == 'secondary_categories' and value is not None:
                # Автоматическое добавление категорий при обновлении
                secondary = list(value) if value else []
                if db_record.record_type == 'disease' and db_record.primary_category_id == 3:
                    if 1 not in secondary:
                        secondary.append(1)
                    if 2 not in secondary:
                        secondary.append(2)
                if db_record.record_type == 'medication':
                    if 1 not in secondary:
                        secondary.append(1)
                setattr(db_record, key, secondary)
            elif value is not None:
                setattr(db_record, key, value)
        db_record.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_cross_record(db: Session, record_id: int):
    db_record = get_cross_record(db, record_id)
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    return False

# ============================================
# CRUD для Партнеров
# ============================================

def get_partners(db: Session, person_id: int):
    return db.query(models_extension.Partner).filter(
        models_extension.Partner.person_id == person_id
    ).order_by(desc(models_extension.Partner.start_date)).all()

def get_partner(db: Session, partner_id: int):
    return db.query(models_extension.Partner).filter(models_extension.Partner.id == partner_id).first()

def create_partner(db: Session, person_id: int, partner_data):
    db_partner = models_extension.Partner(person_id=person_id, **partner_data.model_dump())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

def update_partner(db: Session, partner_id: int, partner_data):
    db_partner = get_partner(db, partner_id)
    if db_partner:
        for key, value in partner_data.model_dump().items():
            if value is not None:
                setattr(db_partner, key, value)
        db_partner.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_partner)
    return db_partner

def delete_partner(db: Session, partner_id: int):
    db_partner = get_partner(db, partner_id)
    if db_partner:
        db.delete(db_partner)
        db.commit()
        return True
    return False

# ============================================
# CRUD для Устройств
# ============================================

def get_devices(db: Session, person_id: int):
    return db.query(models_extension.Device).filter(
        models_extension.Device.person_id == person_id,
        models_extension.Device.is_active == True
    ).order_by(models_extension.Device.created_at.desc()).all()

def get_device(db: Session, device_id: int):
    return db.query(models_extension.Device).filter(models_extension.Device.id == device_id).first()

def create_device(db: Session, person_id: int, device_data):
    db_device = models_extension.Device(person_id=person_id, **device_data.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device(db: Session, device_id: int, device_data):
    db_device = get_device(db, device_id)
    if db_device:
        for key, value in device_data.model_dump().items():
            if value is not None:
                setattr(db_device, key, value)
        db_device.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: int):
    db_device = get_device(db, device_id)
    if db_device:
        db.delete(db_device)
        db.commit()
        return True
    return False

# ============================================
# CRUD для Тегов
# ============================================

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_extension.Tag).order_by(models_extension.Tag.name).offset(skip).limit(limit).all()

def get_tag(db: Session, tag_id: int):
    return db.query(models_extension.Tag).filter(models_extension.Tag.id == tag_id).first()

def create_tag(db: Session, tag_data):
    db_tag = models_extension.Tag(**tag_data.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def add_tag_to_record(db: Session, record_id: int, tag_id: int):
    relation = models_extension.RecordTagRelation(record_id=record_id, tag_id=tag_id)
    db.add(relation)
    db.commit()
    return relation

def remove_tag_from_record(db: Session, record_id: int, tag_id: int):
    relation = db.query(models_extension.RecordTagRelation).filter(
        models_extension.RecordTagRelation.record_id == record_id,
        models_extension.RecordTagRelation.tag_id == tag_id
    ).first()
    if relation:
        db.delete(relation)
        db.commit()
        return True
    return False
