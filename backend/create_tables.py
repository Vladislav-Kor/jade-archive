"""
create_tables.py - Direct table creation script
"""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import models
from database import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables_directly():
    """Create all tables directly without migrations"""
    try:
        engine = create_engine(DATABASE_URL)
        logger.info("Creating tables directly...")
        
        # Drop existing tables first (clean slate)
        logger.info("Dropping existing tables...")
        models.Base.metadata.drop_all(bind=engine)
        logger.info("Tables dropped successfully")
        
        # Create all tables
        logger.info("Creating tables...")
        models.Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tables created: {tables}")
        
        # Insert sample category
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO categories (name, slug, icon, color, description, created_at, updated_at)
                VALUES ('General', 'general', '📁', '#2e7d64', 'General category', NOW(), NOW())
            """))
            conn.commit()
            logger.info("Sample category created")
        
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_tables_directly()