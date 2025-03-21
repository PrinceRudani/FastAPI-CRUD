from typing import List

from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session

from base.config.logger_config import get_logger
from base.db.database import get_db
from base.dto.category.category_dto import CategoryDTO, CategoryResponse
from base.service.category.category_service import CategoryService
from base.utils.custom_exception import AppServices

logger = get_logger()

category_router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "API endpoint not found"}},
)


@category_router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_category(
        category: CategoryDTO = Depends(CategoryDTO.as_form),
        db: Session = Depends(get_db),
):
    try:
        logger.info("Attempting to insert new category: %s",
                    category.category_name)
        result = CategoryService.insert_category(category, db)
        logger.info("Category inserted successfully: %s",
                    category.category_name)
        return result
    except Exception as e:
        logger.exception("Error inserting category")
        return AppServices.handle_exception(e)


@category_router.get(
    "/all", response_model=List[CategoryResponse],
    status_code=status.HTTP_200_OK
)
async def view_category(db: Session = Depends(get_db)):
    try:
        result = CategoryService.get_all_categories(db)
        logger.info("Fetched all (%d) categories", len(result))
        return result
    except Exception as e:
        logger.exception("Error fetching categories")
        return AppServices.handle_exception(e)


@category_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_category(id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Attempting to delete category with ID: %d", id)
        db_category = CategoryService.delete_category(db, id)
        if not db_category:
            logger.warning("Category not found for deletion: ID %d", id)
            return {"message": "Category not found for delete", "id": id}
        logger.info("Category deleted successfully: ID %d", id)
        return {"message": "Category soft-deleted successfully", "id": id}
    except Exception as e:
        logger.exception("Error deleting category")
        return AppServices.handle_exception(e)


@category_router.get(
    "/{id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
async def edit_category(id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Fetching category details for ID: %d", id)
        category_data = CategoryService.get_category_by_id(db, id)
        if not category_data:
            logger.warning("Category not found: ID %d", id)
        else:
            logger.info("Category details fetched successfully: ID %d", id)
        return category_data
    except Exception as e:
        logger.exception("Error fetching category details")
        return AppServices.handle_exception(e)


@category_router.put(
    "/update/{id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
async def update_category(
        id: int,
        category_name: str = Form(...),
        category_description: str = Form(...),
        db: Session = Depends(get_db),
):
    try:
        logger.info("Attempting to update category: ID %d, Name: %s", id,
                    category_name)
        category_dto = CategoryDTO(
            category_name=category_name,
            category_description=category_description
        )
        result = CategoryService.update_category(db, id, category_dto)
        logger.info("Category updated successfully: ID %d, Name: %s", id,
                    category_name)
        return result
    except Exception as e:
        logger.exception("Error updating category")
        return AppServices.handle_exception(e)
