from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://jade_user:jade_password@db:5432/jade_archive")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with retry logic"""
    max_retries = 10
    retry_delay = 3
    
    for i in range(max_retries):
        try:
            print(f"Connecting to database (attempt {i+1}/{max_retries})...")
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            
            Base.metadata.create_all(bind=engine)
            print("Database tables created/verified!")
            return True
        except Exception as e:
            print(f"Connection failed (attempt {i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("Failed to connect to database after all retries")
                raise