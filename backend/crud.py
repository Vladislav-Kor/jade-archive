from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
import models, schemas

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_person_by_short_name(db: Session, short_name: str):
    return db.query(models.Person).filter(models.Person.short_name == short_name).first()

def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).order_by(desc(models.Person.importance)).offset(skip).limit(limit).all()

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.model_dump())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(db: Session, person_id: int, person: schemas.PersonUpdate):
    db_person = get_person(db, person_id)
    if db_person:
        for key, value in person.model_dump().items():
            setattr(db_person, key, value)
        db.commit()
        db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    db_person = get_person(db, person_id)
    if db_person:
        # Delete related relations
        db.query(models.Relation).filter(
            or_(
                models.Relation.parent_id == person_id,
                models.Relation.child_id == person_id
            )
        ).delete()
        # Delete related social media
        db.query(models.SocialMedia).filter(models.SocialMedia.person_id == person_id).delete()
        # Delete related tags
        db.query(models.TagPreference).filter(models.TagPreference.person_id == person_id).delete()
        # Delete person
        db.delete(db_person)
        db.commit()
        return True
    return False

def search_persons(db: Session, query: str):
    return db.query(models.Person).filter(
        or_(
            models.Person.full_name.ilike(f"%{query}%"),
            models.Person.short_name.ilike(f"%{query}%")
        )
    ).order_by(desc(models.Person.importance)).all()

def create_relation(db: Session, relation: schemas.RelationCreate):
    db_relation = models.Relation(**relation.model_dump())
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation

def delete_relation(db: Session, relation_id: int):
    db_relation = db.query(models.Relation).filter(models.Relation.id == relation_id).first()
    if db_relation:
        db.delete(db_relation)
        db.commit()
        return True
    return False

def get_social_media(db: Session, person_id: int):
    return db.query(models.SocialMedia).filter(models.SocialMedia.person_id == person_id).all()

def add_social_media(db: Session, person_id: int, social: schemas.SocialMediaBase):
    db_social = models.SocialMedia(person_id=person_id, **social.model_dump())
    db.add(db_social)
    db.commit()
    db.refresh(db_social)
    return db_social

def delete_social_media(db: Session, social_id: int):
    db_social = db.query(models.SocialMedia).filter(models.SocialMedia.id == social_id).first()
    if db_social:
        db.delete(db_social)
        db.commit()
        return True
    return False

def get_tags(db: Session, person_id: int):
    return db.query(models.TagPreference).filter(models.TagPreference.person_id == person_id).all()

def add_tag(db: Session, person_id: int, tag: schemas.TagPreferenceBase):
    db_tag = models.TagPreference(person_id=person_id, **tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(models.TagPreference).filter(models.TagPreference.id == tag_id).first()
    if db_tag:
        db.delete(db_tag)
        db.commit()
        return True
    return False

def build_tree(db: Session, parent_id: int = 1):
    root_person = get_person(db, parent_id)
    if not root_person:
        return None
    
    root = schemas.TreeNode(
        id=root_person.id,
        name=root_person.full_name,
        short_name=root_person.short_name,
        importance=root_person.importance or 0,
        importance_level=root_person.importance_level or "medium",
        children=[]
    )
    
    relations = db.query(models.Relation).filter(models.Relation.parent_id == parent_id).all()
    
    # Sort children by importance
    children_list = []
    for relation in relations:
        child_person = get_person(db, relation.child_id)
        if child_person:
            children_list.append((child_person, relation.relation_type))
    
    children_list.sort(key=lambda x: x[0].importance or 0, reverse=True)
    
    for child_person, relation_type in children_list:
        child_node = schemas.TreeNode(
            id=child_person.id,
            name=f"{child_person.full_name} ({relation_type})",
            short_name=child_person.short_name,
            importance=child_person.importance or 0,
            importance_level=child_person.importance_level or "medium",
            children=[]
        )
        grandchildren = build_tree(db, child_person.id)
        if grandchildren:
            child_node.children = grandchildren.children
        root.children.append(child_node)
    
    return root