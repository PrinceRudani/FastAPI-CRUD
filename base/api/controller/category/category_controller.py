from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from base.config.logger_config import get_logger
from base.db.database import SessionLocal
from base.dto.category.category_dto import CategoryDTO
from base.service.category.category_service import CategoryService
from base.utils.custom_exception import AppServices

logger = get_logger()

category_router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "API endpoint not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post("/insert")
async def insert_category_controller(category: CategoryDTO,
                                     db: Session = Depends(get_db)):
    try:
        logger.info("Attempting to insert new category: %s",
                    category.category_name)
        result = CategoryService.insert_category_service(category, db)
        return result
    except Exception as exception:
        logger.exception("Error inserting category")
        return AppServices.handle_exception(exception)


@category_router.get("/all")
async def view_category_controller(db: Session = Depends(get_db)):
    try:
        result = CategoryService.get_all_categories_service(db)
        logger.info(result)
        return result
    except Exception as exception:
        logger.exception("Error fetching categories")
        return AppServices.handle_exception(exception)


@category_router.delete("/delete/{id}")
async def delete_category_controller(id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Attempting to delete category with ID: %d", id)
        result = CategoryService.delete_category_service(id, db)
        return result
    except Exception as exception:
        logger.exception("Error deleting category")
        return AppServices.handle_exception(exception)


@category_router.get("/get/{id}")
async def edit_category_controller(id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Fetching category details for ID: %d", id)
        result = CategoryService.get_category_by_id_service(id, db)
        return result
    except Exception as exception:
        logger.exception("Error fetching category details")
        return AppServices.handle_exception(exception)


@category_router.put("/update/{id}")
async def update_category_controller(id: int, category_dto: CategoryDTO,
                                     db: Session = Depends(get_db)):
    try:
        logger.info("Attempting to update category: ID %d, Name: %s", id,
                    category_dto.category_name)
        result = CategoryService.update_category_service(id, category_dto, db)
        return result
    except Exception as exception:
        logger.exception("Error updating category")
        return AppServices.handle_exception(exception)
