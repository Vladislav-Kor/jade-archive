from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import engine, get_db, init_db

# Initialize database
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Error initializing database: {e}")

app = FastAPI(title="Jade Archive API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Health Check
# ============================================

@app.get("/")
def root():
    return {"message": "Jade Archive API is running"}

@app.get("/api/health")
def health():
    return {"status": "ok", "database": "connected"}

# ============================================
# Person Endpoints
# ============================================

@app.post("/api/persons", response_model=schemas.PersonResponse, status_code=201)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    existing = crud.get_person_by_short_name(db, person.short_name)
    if existing:
        raise HTTPException(status_code=400, detail="Short name already exists")
    return crud.create_person(db, person)

@app.get("/api/persons", response_model=List[schemas.PersonResponse])
def list_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit)
    for person in persons:
        person.social_media = crud.get_social_media(db, person.id)
        person.tags_prefs = crud.get_tags(db, person.id)
        person.digital_accounts = crud.get_digital_accounts(db, person.id)
    return persons

@app.get("/api/persons/{person_id}", response_model=schemas.PersonResponse)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    person.social_media = crud.get_social_media(db, person_id)
    person.tags_prefs = crud.get_tags(db, person_id)
    person.digital_accounts = crud.get_digital_accounts(db, person_id)
    return person

@app.put("/api/persons/{person_id}", response_model=schemas.PersonResponse)
def update_person(person_id: int, person: schemas.PersonUpdate, db: Session = Depends(get_db)):
    updated = crud.update_person(db, person_id, person)
    if not updated:
        raise HTTPException(status_code=404, detail="Person not found")
    updated.social_media = crud.get_social_media(db, person_id)
    updated.tags_prefs = crud.get_tags(db, person_id)
    updated.digital_accounts = crud.get_digital_accounts(db, person_id)
    return updated

@app.delete("/api/persons/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    if not crud.delete_person(db, person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": "Person deleted"}

@app.get("/api/search")
def search_persons(q: str, db: Session = Depends(get_db)):
    persons = crud.search_persons(db, q)
    for person in persons:
        person.social_media = crud.get_social_media(db, person.id)
        person.tags_prefs = crud.get_tags(db, person.id)
        person.digital_accounts = crud.get_digital_accounts(db, person.id)
    return persons

# ============================================
# Tree Endpoint
# ============================================

@app.get("/api/tree", response_model=schemas.TreeNode)
def get_tree(db: Session = Depends(get_db)):
    # Get or create root
    root = crud.get_person_by_short_name(db, "me")
    if not root:
        root = crud.get_person(db, 1)
    if not root:
        root = crud.create_person(db, schemas.PersonCreate(
            full_name="Моя учетная запись",
            short_name="me",
            importance=10,
            importance_level="critical",
            notes="Корневой пользователь"
        ))
    
    tree = crud.build_tree(db, root.id)
    if not tree:
        tree = schemas.TreeNode(
            id=root.id,
            name=root.full_name,
            short_name=root.short_name,
            importance=root.importance or 0,
            importance_level=root.importance_level or "medium",
            children=[]
        )
    return tree

# ============================================
# Relation Endpoints
# ============================================

@app.get("/api/relations", response_model=List[schemas.RelationResponse])
def get_relations(db: Session = Depends(get_db)):
    return db.query(models.Relation).all()

@app.get("/api/persons/{person_id}/relations")
def get_person_relations(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    relations_as_parent = db.query(models.Relation).filter(models.Relation.parent_id == person_id).all()
    relations_as_child = db.query(models.Relation).filter(models.Relation.child_id == person_id).all()
    
    result = []
    for rel in relations_as_parent:
        child = crud.get_person(db, rel.child_id)
        result.append({
            "id": rel.id,
            "direction": "outgoing",
            "person_name": child.full_name if child else "Unknown",
            "person_id": rel.child_id,
            "relation_type": rel.relation_type
        })
    
    for rel in relations_as_child:
        parent = crud.get_person(db, rel.parent_id)
        result.append({
            "id": rel.id,
            "direction": "incoming",
            "person_name": parent.full_name if parent else "Unknown",
            "person_id": rel.parent_id,
            "relation_type": rel.relation_type
        })
    
    return result

@app.post("/api/relations", response_model=schemas.RelationResponse)
def create_relation(relation: schemas.RelationCreate, db: Session = Depends(get_db)):
    parent = crud.get_person(db, relation.parent_id)
    child = crud.get_person(db, relation.child_id)
    
    if not parent:
        raise HTTPException(status_code=404, detail=f"Parent person with id {relation.parent_id} not found")
    if not child:
        raise HTTPException(status_code=404, detail=f"Child person with id {relation.child_id} not found")
    
    if relation.parent_id == relation.child_id:
        raise HTTPException(status_code=400, detail="Cannot create relation with self")
    
    existing = db.query(models.Relation).filter(
        models.Relation.parent_id == relation.parent_id,
        models.Relation.child_id == relation.child_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Relation already exists: {parent.full_name} -> {child.full_name} ({existing.relation_type})"
        )
    
    reverse_existing = db.query(models.Relation).filter(
        models.Relation.parent_id == relation.child_id,
        models.Relation.child_id == relation.parent_id
    ).first()
    
    if reverse_existing:
        raise HTTPException(
            status_code=400,
            detail=f"Reverse relation already exists: {child.full_name} -> {parent.full_name} ({reverse_existing.relation_type})"
        )
    
    return crud.create_relation(db, relation)

@app.delete("/api/relations/{relation_id}")
def delete_relation(relation_id: int, db: Session = Depends(get_db)):
    relation = db.query(models.Relation).filter(models.Relation.id == relation_id).first()
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    
    if not crud.delete_relation(db, relation_id):
        raise HTTPException(status_code=404, detail="Relation not found")
    return {"message": "Relation deleted"}

# ============================================
# Social Media Endpoints
# ============================================

@app.post("/api/persons/{person_id}/social")
def add_social_media(person_id: int, social: schemas.SocialMediaBase, db: Session = Depends(get_db)):
    return crud.add_social_media(db, person_id, social)

@app.delete("/api/social/{social_id}")
def delete_social_media(social_id: int, db: Session = Depends(get_db)):
    if not crud.delete_social_media(db, social_id):
        raise HTTPException(status_code=404, detail="Social media entry not found")
    return {"message": "Social media deleted"}

# ============================================
# Tags Endpoints
# ============================================

@app.post("/api/persons/{person_id}/tags")
def add_tag(person_id: int, tag: schemas.TagPreferenceBase, db: Session = Depends(get_db)):
    return crud.add_tag(db, person_id, tag)

@app.delete("/api/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    if not crud.delete_tag(db, tag_id):
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted"}

# ============================================
# Digital Accounts Endpoints
# ============================================

@app.get("/api/persons/{person_id}/digital-accounts", response_model=List[schemas.DigitalAccountResponse])
def get_person_digital_accounts(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_digital_accounts(db, person_id)

@app.get("/api/digital-accounts/{account_id}", response_model=schemas.DigitalAccountResponse)
def get_digital_account(account_id: int, db: Session = Depends(get_db)):
    """Получить цифровой аккаунт по ID для редактирования"""
    account = crud.get_digital_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Digital account not found")
    return account

@app.post("/api/persons/{person_id}/digital-accounts", response_model=schemas.DigitalAccountResponse)
def create_digital_account(
    person_id: int, 
    account: schemas.DigitalAccountCreate, 
    db: Session = Depends(get_db)
):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.create_digital_account(db, person_id, account)

@app.put("/api/digital-accounts/{account_id}", response_model=schemas.DigitalAccountResponse)
def update_digital_account(
    account_id: int, 
    account: schemas.DigitalAccountUpdate, 
    db: Session = Depends(get_db)
):
    updated = crud.update_digital_account(db, account_id, account)
    if not updated:
        raise HTTPException(status_code=404, detail="Digital account not found")
    return updated

@app.delete("/api/digital-accounts/{account_id}")
def delete_digital_account(account_id: int, db: Session = Depends(get_db)):
    if not crud.delete_digital_account(db, account_id):
        raise HTTPException(status_code=404, detail="Digital account not found")
    return {"message": "Digital account deleted"}

# ============================================
# Startup Event - Create Sample Data
# ============================================

@app.on_event("startup")
def startup_event():
    print("Starting Jade Archive API...")
    try:
        db = next(get_db())
        persons = crud.get_persons(db)
        if len(persons) == 0:
            print("Creating sample data...")
            
            me = crud.create_person(db, schemas.PersonCreate(
                full_name="Моя учетная запись",
                short_name="me",
                importance=10,
                importance_level="critical",
                notes="Корневой пользователь"
            ))
            
            john = crud.create_person(db, schemas.PersonCreate(
                full_name="Иван Петров",
                short_name="ivan",
                phone="+7 999 123-45-67",
                email="ivan@example.com",
                height=180,
                weight=75,
                blood_type="A+",
                importance=8,
                importance_level="high",
                notes="Друг с работы, любит шахматы"
            ))
            
            maria = crud.create_person(db, schemas.PersonCreate(
                full_name="Мария Сидорова",
                short_name="maria",
                phone="+7 999 765-43-21",
                email="maria@example.com",
                height=165,
                weight=60,
                blood_type="O+",
                importance=5,
                importance_level="medium",
                notes="Коллега, отличный дизайнер"
            ))
            
            crud.create_relation(db, schemas.RelationCreate(
                parent_id=me.id, child_id=john.id, relation_type="Друг"
            ))
            crud.create_relation(db, schemas.RelationCreate(
                parent_id=me.id, child_id=maria.id, relation_type="Коллега"
            ))
            
            crud.add_tag(db, john.id, schemas.TagPreferenceBase(
                category="Favorite Color", value="Синий"
            ))
            crud.add_tag(db, john.id, schemas.TagPreferenceBase(
                category="Hobby", value="Шахматы"
            ))
            
            crud.add_social_media(db, john.id, schemas.SocialMediaBase(
                platform="Telegram", link="https://t.me/ivan"
            ))
            
            print(f"Sample data created! Total persons: {len(crud.get_persons(db))}")
        else:
            print(f"Database already has {len(persons)} persons")
    except Exception as e:
        print(f"Error creating sample data: {e}")