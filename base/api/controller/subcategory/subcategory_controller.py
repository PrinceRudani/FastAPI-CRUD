import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from base.dto.subcategory.subcategory_dto import SubcategoryDTO
from base.service.subcategory.subcategory_service import SubcategoryService
from base.utils.custom_exception import AppServices

# Configure logger
logger = logging.getLogger("subcategory")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

subcategory_router = APIRouter(
    prefix="/subcategory",
    tags=["Subcategory"],
    responses={404: {"description": "API endpoint not found"}},
)


@subcategory_router.post("/insert")
async def insert_subcategory_controller(subcategory: SubcategoryDTO):
    try:
        logger.info("Inserting new subcategory: %s", subcategory.subcategory_name)
        return SubcategoryService.insert_subcategory_service(subcategory, db)
    except Exception as e:
        logger.error("Error inserting subcategory: %s", str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.get("/all")
async def view_subcategory_controller():
    try:
        logger.info("Fetching all subcategories")
        return SubcategoryService.get_all_subcategories_service(db)
    except Exception as e:
        logger.error("Error fetching subcategories: %s", str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.delete("/delete/{id}")
async def delete_subcategory_controller(id: int):
    try:
        logger.info("Deleting subcategory with ID: %d", id)
        return SubcategoryService.delete_subcategory_service(id, db)
    except Exception as e:
        logger.error("Error deleting subcategory with ID %d: %s", id, str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.get("/get/{id}")
async def get_subcategory_by_id_controller(id: int):
    try:
        logger.info("Fetching subcategory with ID: %d", id)
        return SubcategoryService.get_subcategory_by_id_service(id, db)
    except Exception as e:
        logger.error("Error fetching subcategory with ID %d: %s", id, str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.put("/update/{id}")
async def update_subcategory_controller(id: int, subcategory: SubcategoryDTO):
    try:
        logger.info("Updating subcategory with ID: %d", id)
        return SubcategoryService.update_subcategory_service(id, subcategory, db)
    except Exception as e:
        logger.error("Error updating subcategory with ID %d: %s", id, str(e))
        raise AppServices.handle_exception(e, is_raise=True)
