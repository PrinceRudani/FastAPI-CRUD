import logging

from fastapi import APIRouter, Response

from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dto.subcategory.subcategory_dto import SubcategoryDTO, UpdateSubcategoryDTO
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
def insert_subcategory_controller(subcategory_dto: SubcategoryDTO, response: Response):
    try:
        if not subcategory_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )
        logger.info("Inserting new subcategory: %s", subcategory_dto.subcategory_name)
        result = SubcategoryService.insert_subcategory_service(subcategory_dto)
        return result

    except Exception as e:
        logger.error("Error inserting subcategory: %s", str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.get("/all")
def view_subcategory_controller():
    try:
        logger.info("Fetching all subcategories")
        response_payload = SubcategoryService.get_all_subcategories_service()
        return response_payload
    except Exception as e:
        logger.error("Error fetching subcategories: %s", str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.delete("/delete/{id}")
def delete_subcategory_controller(id: int):
    try:
        logger.info("Deleting subcategory with ID: %d", id)
        response_payload = SubcategoryService.delete_subcategory_service(id)
        return response_payload
    except Exception as e:
        logger.error("Error deleting subcategory with ID %d: %s", id, str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.get("/get/{id}")
def get_subcategory_by_id_controller(id: int):
    try:
        logger.info("Fetching subcategory with ID: %d", id)
        response_payload = SubcategoryService.get_subcategory_by_id_service(id)
        return response_payload
    except Exception as e:
        logger.error("Error fetching subcategory with ID %d: %s", id, str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.put("/update/{id}")
def update_subcategory_controller(update_subcategory_dto: UpdateSubcategoryDTO):
    try:
        logger.info("Updating subcategory with ID")
        response_payload = SubcategoryService.update_subcategory_service(
            update_subcategory_dto
        )
        return response_payload
    except Exception as e:
        logger.error("Error updating subcategory with ")
        raise AppServices.handle_exception(e, is_raise=True)
