"""
api_extension.py - Extension routes for Jade Archive API
Production-ready with full error handling
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import get_db
import models
import schemas
import crud

logger = logging.getLogger(__name__)

def register_extension_routes(app: FastAPI):
    """
    Register all extension routes for the API
    """
    
    @app.get(
        "/api/categories",
        response_model=List[schemas.CategoryResponse],
        summary="Get all categories"
    )
    def get_categories(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
    ):
        """
        Get all categories with pagination
        """
        try:
            categories = db.query(models.Category).offset(skip).limit(limit).all()
            
            # Convert to response models
            result = []
            for category in categories:
                result.append(schemas.CategoryResponse(
                    id=category.id,
                    name=category.name,
                    slug=category.slug,
                    icon=category.icon,
                    color=category.color,
                    description=category.description,
                    created_at=category.created_at,
                    updated_at=category.updated_at
                ))
            
            return result
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get categories: {str(e)}"
            )
    
    # /tree регистрируется раньше /{category_id}, иначе "tree" разбирается как id и даёт 422.
    @app.get(
        "/api/categories/tree",
        response_model=List[dict],
        summary="Get categories as tree"
    )
    def get_category_tree(
        db: Session = Depends(get_db)
    ):
        """
        Get categories as hierarchical tree
        """
        try:
            categories = db.query(models.Category).all()
            
            result = []
            for category in categories:
                result.append({
                    "id": category.id,
                    "name": category.name,
                    "slug": category.slug,
                    "icon": category.icon,
                    "color": category.color,
                    "description": category.description,
                    "created_at": category.created_at,
                    "updated_at": category.updated_at
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting category tree: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get category tree: {str(e)}"
            )
    
    @app.get(
        "/api/categories/{category_id}",
        response_model=schemas.CategoryResponse,
        summary="Get category by ID"
    )
    def get_category(
        category_id: int,
        db: Session = Depends(get_db)
    ):
        """
        Get category by ID
        """
        try:
            category = db.query(models.Category).filter(
                models.Category.id == category_id
            ).first()
            
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {category_id} not found"
                )
            
            return schemas.CategoryResponse(
                id=category.id,
                name=category.name,
                slug=category.slug,
                icon=category.icon,
                color=category.color,
                description=category.description,
                created_at=category.created_at,
                updated_at=category.updated_at
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting category {category_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get category: {str(e)}"
            )
    
    @app.post(
        "/api/categories",
        response_model=schemas.CategoryResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Create category"
    )
    def create_category(
        category: schemas.CategoryCreate,
        db: Session = Depends(get_db)
    ):
        """
        Create a new category
        """
        try:
            # Check if slug exists
            existing = db.query(models.Category).filter(
                models.Category.slug == category.slug
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Category with slug '{category.slug}' already exists"
                )
            
            db_category = models.Category(
                name=category.name.strip(),
                slug=category.slug.strip(),
                icon=category.icon,
                color=category.color,
                description=category.description
            )
            
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            
            logger.info(f"Created category: {category.name}")
            
            return schemas.CategoryResponse(
                id=db_category.id,
                name=db_category.name,
                slug=db_category.slug,
                icon=db_category.icon,
                color=db_category.color,
                description=db_category.description,
                created_at=db_category.created_at,
                updated_at=db_category.updated_at
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create category: {str(e)}"
            )
    
    @app.put(
        "/api/categories/{category_id}",
        response_model=schemas.CategoryResponse,
        summary="Update category"
    )
    def update_category(
        category_id: int,
        category: schemas.CategoryUpdate,
        db: Session = Depends(get_db)
    ):
        """
        Update an existing category
        """
        try:
            db_category = db.query(models.Category).filter(
                models.Category.id == category_id
            ).first()
            
            if not db_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {category_id} not found"
                )
            
            # Check slug uniqueness if changed
            if category.slug and category.slug != db_category.slug:
                existing = db.query(models.Category).filter(
                    models.Category.slug == category.slug
                ).first()
                
                if existing and existing.id != category_id:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Category with slug '{category.slug}' already exists"
                    )
            
            update_data = category.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if isinstance(value, str) and value:
                    value = value.strip()
                setattr(db_category, key, value)
            
            db.commit()
            db.refresh(db_category)
            
            logger.info(f"Updated category: {category_id}")
            
            return schemas.CategoryResponse(
                id=db_category.id,
                name=db_category.name,
                slug=db_category.slug,
                icon=db_category.icon,
                color=db_category.color,
                description=db_category.description,
                created_at=db_category.created_at,
                updated_at=db_category.updated_at
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating category {category_id}: {e}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update category: {str(e)}"
            )
    
    @app.delete(
        "/api/categories/{category_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete category"
    )
    def delete_category(
        category_id: int,
        db: Session = Depends(get_db)
    ):
        """
        Delete a category
        """
        try:
            db_category = db.query(models.Category).filter(
                models.Category.id == category_id
            ).first()
            
            if not db_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {category_id} not found"
                )
            
            # Check if category has cross records
            records_count = db.query(models.CrossRecord).filter(
                models.CrossRecord.primary_category_id == category_id
            ).count()
            
            if records_count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot delete category with {records_count} records. Reassign records first."
                )
            
            db.delete(db_category)
            db.commit()
            
            logger.info(f"Deleted category: {category_id}")
            return None
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting category {category_id}: {e}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete category: {str(e)}"
            )
    
    logger.info("Extension routes registered successfully")