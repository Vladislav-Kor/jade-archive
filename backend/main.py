from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from schemas import (
    PersonResponse, PersonCreate, PersonUpdate,
    RelationResponse, RelationCreate,
    SocialMediaResponse, SocialMediaBase,
    TagPreferenceResponse, TagPreferenceBase,
    DigitalAccountResponse, DigitalAccountCreate, DigitalAccountUpdate,
    RealEstateResponse, RealEstateCreate, RealEstateUpdate,
    VehicleResponse, VehicleCreate, VehicleUpdate,
    CaseResponse, CaseCreate, CaseUpdate,
    MedicalRecordResponse, MedicalRecordCreate, MedicalRecordUpdate,
    CrossRecordResponse, CrossRecordCreate, CrossRecordUpdate,
    PartnerResponse, PartnerCreate, PartnerUpdate,
    DeviceResponse, DeviceCreate, DeviceUpdate,
    CategoryResponse, CategoryCreate, CategoryUpdate,
    TagResponse, TagCreate, TagUpdate,
    TreeNode
)
from database import engine, get_db, init_db
from api_extension import register_extension_routes

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
# РЕГИСТРАЦИЯ НОВЫХ ЭНДПОИНТОВ
# ============================================
register_extension_routes(app)

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

@app.get("/api/persons", response_model=List[schemas.PersonListItem])
def list_persons(skip: int = 0, limit: int = Query(1000, ge=1, le=1000), db: Session = Depends(get_db)):
    # Список для боковой панели и выпадающих списков: без вложенных коллекций
    # (раньше здесь уходили аккаунты с паролями всех людей и по 3 запроса на человека).
    return crud.get_persons(db, skip=skip, limit=limit)

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

@app.get("/api/search", response_model=List[schemas.PersonListItem])
def search_persons(q: str, db: Session = Depends(get_db)):
    return crud.search_persons(db, q)

# ============================================
# Tree Endpoint
# ============================================

@app.get("/api/tree", response_model=schemas.TreeNode)
def get_tree(db: Session = Depends(get_db)):
    root = crud.get_person_by_short_name(db, "me")
    if not root:
        root = crud.get_person(db, 1)
    if not root:
        root = crud.create_person(db, schemas.PersonCreate(
            full_name="My Account",
            short_name="me",
            importance=10,
            importance_level="critical",
            notes="Root user"
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
        result.append({"id": rel.id, "direction": "outgoing", "person_name": child.full_name if child else "Unknown", "person_id": rel.child_id, "relation_type": rel.relation_type})
    for rel in relations_as_child:
        parent = crud.get_person(db, rel.parent_id)
        result.append({"id": rel.id, "direction": "incoming", "person_name": parent.full_name if parent else "Unknown", "person_id": rel.parent_id, "relation_type": rel.relation_type})
    return result

@app.post("/api/relations", response_model=schemas.RelationResponse, status_code=201)
def create_relation(relation: schemas.RelationCreate, db: Session = Depends(get_db)):
    parent = crud.get_person(db, relation.parent_id)
    child = crud.get_person(db, relation.child_id)
    if not parent or not child:
        raise HTTPException(status_code=404, detail="Person not found")
    if relation.parent_id == relation.child_id:
        raise HTTPException(status_code=400, detail="Cannot create relation with self")
    return crud.create_relation(db, relation)

@app.delete("/api/relations/{relation_id}")
def delete_relation(relation_id: int, db: Session = Depends(get_db)):
    if not crud.delete_relation(db, relation_id):
        raise HTTPException(status_code=404, detail="Relation not found")
    return {"message": "Relation deleted"}

# ============================================
# Social Media Endpoints
# ============================================

@app.get("/api/persons/{person_id}/social", response_model=List[schemas.SocialMediaResponse])
def get_person_social_media(person_id: int, db: Session = Depends(get_db)):
    if not crud.get_person(db, person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_social_media(db, person_id)

@app.post("/api/persons/{person_id}/social", response_model=schemas.SocialMediaResponse, status_code=201)
def add_social_media(person_id: int, social: schemas.SocialMediaBase, db: Session = Depends(get_db)):
    if not crud.get_person(db, person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.add_social_media(db, person_id, social)

@app.put("/api/social/{social_id}", response_model=schemas.SocialMediaResponse)
def update_social_media(social_id: int, social: schemas.SocialMediaBase, db: Session = Depends(get_db)):
    updated = crud.update_social_media(db, social_id, social)
    if not updated:
        raise HTTPException(status_code=404, detail="Social media entry not found")
    return updated

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
    account = crud.get_digital_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Digital account not found")
    return account

@app.post("/api/persons/{person_id}/digital-accounts", response_model=schemas.DigitalAccountResponse, status_code=201)
def create_digital_account(person_id: int, account: schemas.DigitalAccountCreate, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.create_digital_account(db, person_id, account)

@app.put("/api/digital-accounts/{account_id}", response_model=schemas.DigitalAccountResponse)
def update_digital_account(account_id: int, account: schemas.DigitalAccountUpdate, db: Session = Depends(get_db)):
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
# Cases Endpoints
# ============================================

@app.get("/api/persons/{person_id}/cases", response_model=List[schemas.CaseResponse])
def get_person_cases(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_cases(db, person_id)

@app.get("/api/cases/{case_id}", response_model=schemas.CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = crud.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@app.post("/api/persons/{person_id}/cases", response_model=schemas.CaseResponse, status_code=201)
def create_case(person_id: int, case: schemas.CaseCreate, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.create_case(db, person_id, case)

@app.put("/api/cases/{case_id}", response_model=schemas.CaseResponse)
def update_case(case_id: int, case: schemas.CaseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_case(db, case_id, case)
    if not updated:
        raise HTTPException(status_code=404, detail="Case not found")
    return updated

@app.delete("/api/cases/{case_id}")
def delete_case(case_id: int, db: Session = Depends(get_db)):
    if not crud.delete_case(db, case_id):
        raise HTTPException(status_code=404, detail="Case not found")
    return {"message": "Case deleted"}

# ============================================
# Medical Records Endpoints
# ============================================

@app.get("/api/persons/{person_id}/medical", response_model=List[schemas.MedicalRecordResponse])
def get_person_medical_records(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_medical_records(db, person_id)

@app.get("/api/medical/{record_id}", response_model=schemas.MedicalRecordResponse)
def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_medical_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record

@app.post("/api/persons/{person_id}/medical", response_model=schemas.MedicalRecordResponse, status_code=201)
def create_medical_record(person_id: int, record: schemas.MedicalRecordCreate, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.create_medical_record(db, person_id, record)

@app.put("/api/medical/{record_id}", response_model=schemas.MedicalRecordResponse)
def update_medical_record(record_id: int, record: schemas.MedicalRecordUpdate, db: Session = Depends(get_db)):
    updated = crud.update_medical_record(db, record_id, record)
    if not updated:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return updated

@app.delete("/api/medical/{record_id}")
def delete_medical_record(record_id: int, db: Session = Depends(get_db)):
    if not crud.delete_medical_record(db, record_id):
        raise HTTPException(status_code=404, detail="Medical record not found")
    return {"message": "Medical record deleted"}

# ============================================
# Real Estate Endpoints
# ============================================

@app.get("/api/persons/{person_id}/real-estate", response_model=List[schemas.RealEstateResponse])
def get_person_real_estate(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_real_estate(db, person_id)

@app.get("/api/real-estate/{property_id}", response_model=schemas.RealEstateResponse)
def get_real_estate_item(property_id: int, db: Session = Depends(get_db)):
    property_item = crud.get_real_estate_item(db, property_id)
    if not property_item:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_item

@app.post("/api/persons/{person_id}/real-estate", response_model=schemas.RealEstateResponse, status_code=201)
def create_real_estate(person_id: int, property_data: schemas.RealEstateCreate, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.create_real_estate(db, person_id, property_data)

@app.put("/api/real-estate/{property_id}", response_model=schemas.RealEstateResponse)
def update_real_estate(property_id: int, property_data: schemas.RealEstateUpdate, db: Session = Depends(get_db)):
    updated = crud.update_real_estate(db, property_id, property_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated

@app.delete("/api/real-estate/{property_id}")
def delete_real_estate(property_id: int, db: Session = Depends(get_db)):
    if not crud.delete_real_estate(db, property_id):
        raise HTTPException(status_code=404, detail="Property not found")
    return {"message": "Property deleted"}

# ============================================
# Vehicle Endpoints
# ============================================

@app.get("/api/persons/{person_id}/vehicles", response_model=List[schemas.VehicleResponse])
def get_person_vehicles(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_vehicles(db, person_id)

@app.get("/api/vehicles/{vehicle_id}", response_model=schemas.VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = crud.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.post("/api/persons/{person_id}/vehicles", response_model=schemas.VehicleResponse, status_code=201)
def create_vehicle(person_id: int, vehicle_data: schemas.VehicleCreate, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.create_vehicle(db, person_id, vehicle_data)

@app.put("/api/vehicles/{vehicle_id}", response_model=schemas.VehicleResponse)
def update_vehicle(vehicle_id: int, vehicle_data: schemas.VehicleUpdate, db: Session = Depends(get_db)):
    updated = crud.update_vehicle(db, vehicle_id, vehicle_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated

@app.delete("/api/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    if not crud.delete_vehicle(db, vehicle_id):
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"message": "Vehicle deleted"}

# ============================================
# Partner Endpoints
# ============================================

@app.get("/api/persons/{person_id}/partners", response_model=List[schemas.PartnerResponse])
def get_person_partners(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_partners(db, person_id)

@app.get("/api/partners/{partner_id}", response_model=schemas.PartnerResponse)
def get_partner(partner_id: int, db: Session = Depends(get_db)):
    partner = crud.get_partner(db, partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner

@app.post("/api/persons/{person_id}/partners", response_model=schemas.PartnerResponse, status_code=201)
def create_partner(person_id: int, partner_data: schemas.PartnerCreate, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    if partner_data.person_id != person_id:
        raise HTTPException(status_code=400, detail="person_id mismatch")
    partner = crud.get_person(db, partner_data.partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner person not found")
    return crud.create_partner(db, partner_data)

@app.put("/api/partners/{partner_id}", response_model=schemas.PartnerResponse)
def update_partner(partner_id: int, partner_data: schemas.PartnerUpdate, db: Session = Depends(get_db)):
    updated = crud.update_partner(db, partner_id, partner_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Partner not found")
    return updated

@app.delete("/api/partners/{partner_id}")
def delete_partner(partner_id: int, db: Session = Depends(get_db)):
    if not crud.delete_partner(db, partner_id):
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"message": "Partner deleted"}

# ============================================
# Device Endpoints
# ============================================

@app.get("/api/persons/{person_id}/devices", response_model=List[schemas.DeviceResponse])
def get_person_devices(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_devices(db, person_id)

@app.get("/api/devices/{device_id}", response_model=schemas.DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = crud.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@app.post("/api/persons/{person_id}/devices", response_model=schemas.DeviceResponse, status_code=201)
def create_device(person_id: int, device_data: schemas.DeviceCreate, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.create_device(db, device_data)

@app.put("/api/devices/{device_id}", response_model=schemas.DeviceResponse)
def update_device(device_id: int, device_data: schemas.DeviceUpdate, db: Session = Depends(get_db)):
    updated = crud.update_device(db, device_id, device_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated

@app.delete("/api/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    if not crud.delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted"}

# ============================================
# CROSS RECORDS ENDPOINTS
# ============================================

@app.get("/api/cross-records/{record_id}", response_model=schemas.CrossRecordResponse)
def get_cross_record(record_id: int, db: Session = Depends(get_db)):
    """Получить запись по ID"""
    print(f"GET /api/cross-records/{record_id}")
    record = crud.get_cross_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.get("/api/persons/{person_id}/cross-records", response_model=List[schemas.CrossRecordResponse])
def get_person_cross_records(person_id: int, db: Session = Depends(get_db)):
    """Получить все записи человека"""
    print(f"GET /api/persons/{person_id}/cross-records")
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return crud.get_cross_records(db, person_id)

@app.post("/api/cross-records", response_model=schemas.CrossRecordResponse, status_code=201)
def create_cross_record(record: schemas.CrossRecordCreate, db: Session = Depends(get_db)):
    """Создать новую запись"""
    print(f"POST /api/cross-records")
    print(f"Data: {record}")
    
    person = crud.get_person(db, record.person_id)
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with id {record.person_id} not found")
    
    category = crud.get_category(db, record.primary_category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {record.primary_category_id} not found")
    
    try:
        result = crud.create_cross_record(db, record)
        print(f"Record created: {result.id}")
        return result
    except Exception as e:
        print(f"Error creating record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/cross-records/{record_id}", response_model=schemas.CrossRecordResponse)
def update_cross_record(record_id: int, record: schemas.CrossRecordUpdate, db: Session = Depends(get_db)):
    """Обновить запись"""
    print(f"PUT /api/cross-records/{record_id}")
    updated = crud.update_cross_record(db, record_id, record)
    if not updated:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated

@app.delete("/api/cross-records/{record_id}")
def delete_cross_record(record_id: int, db: Session = Depends(get_db)):
    """Удалить запись"""
    print(f"DELETE /api/cross-records/{record_id}")
    if not crud.delete_cross_record(db, record_id):
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted"}

# Категории — в api_extension.py (register_extension_routes): там единственная реализация.

# ============================================
# Startup Event
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
                full_name="My Account",
                short_name="me",
                importance=10,
                importance_level="critical",
                notes="Root user"
            ))
            print(f"Sample data created! Total persons: {len(crud.get_persons(db))}")
        else:
            print(f"Database already has {len(persons)} persons")
    except Exception as e:
        print(f"Error creating sample data: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
