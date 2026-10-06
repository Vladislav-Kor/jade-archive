import os
import time
import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import pymysql

pymysql.install_as_MySQLdb()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://jade_user:jade_password@db:3306/jade_archive?charset=utf8mb4")

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,
        "autocommit": False,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(retry_count=5, retry_delay=5):
    for attempt in range(retry_count):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{retry_count})")
            with engine.connect() as conn:
                result = conn.execute(text("SELECT DATABASE()"))
                db_name = result.scalar()
                logger.info(f"Connected to database: {db_name}")
                conn.execute(text("SET NAMES utf8mb4"))
                conn.execute(text("SET CHARACTER SET utf8mb4"))
                conn.execute(text("SET character_set_connection = utf8mb4"))
            
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            logger.info(f"Existing tables: {existing_tables}")
            
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully!")
            
            with engine.connect() as conn:
                tables = conn.execute(text("SHOW TABLES"))
                table_list = [row[0] for row in tables]
                logger.info(f"Final tables: {table_list}")
            
            return True
            
        except OperationalError as e:
            logger.warning(f"Database connection failed (attempt {attempt + 1}/{retry_count}): {e}")
            if attempt < retry_count - 1:
                logger.info(f"Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to database after {retry_count} attempts")
                raise
        except Exception as e:
            logger.error(f"Unexpected error during database initialization: {e}")
            raise
    
    return False

def check_db_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

def drop_all_tables():
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully!")
        return True
    except Exception as e:
        logger.error(f"Error dropping tables: {e}")
        return False
