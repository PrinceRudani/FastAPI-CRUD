from fastapi import APIRouter, Response

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dto.category.category_dto import CategoryDTO, UpdateCategoryDTO
from base.service.category.category_service import CategoryService
from base.utils.custom_exception import AppServices

logger = get_logger()

category_router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "API endpoint not found"}},
)


@category_router.post("/insert")
async def insert_category_controller(category_dto: CategoryDTO,
                                     response: Response):
    try:
        if not category_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )
        logger.info("Attempting to insert new category: %s",
                    category_dto.category_name)
        result = CategoryService.insert_category_service(category_dto)
        return AppServices.app_response(
            HttpStatusCodeEnum.CREATED.value,
            ResponseMessageEnum.INSERT_DATA.value,
            success=True,
            data=result,
        )
    except Exception as exception:
        logger.exception("Error inserting category")
        return AppServices.handle_exception(exception)


@category_router.get("/all")
async def view_category_controller(response: Response):
    try:
        response_payload = CategoryService.get_all_categories_service()

        if not response_payload:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=True,
                data={},
            )

        logger.info(f"Response for verify_member is {response_payload}")
        return AppServices.app_response(
            HttpStatusCodeEnum.OK.value,
            ResponseMessageEnum.GET_DATA.value,
            success=True,
            data=response_payload,
        )

    except Exception as exception:
        logger.exception("Error fetching categories")
        return AppServices.handle_exception(exception)


@category_router.delete("/delete/{id}")
async def delete_category_controller(id: int, response: Response):
    try:
        response_payload = CategoryService.delete_category_service(id)

        if not response_payload:
            logger.warning("Category not found: ID %d", id)
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )
        logger.info("Attempting to delete category with ID: %d", id)
        return AppServices.app_response(
            HttpStatusCodeEnum.OK.value,
            ResponseMessageEnum.DELETE_DATA.value,
            success=True,
            data=response_payload,
        )

    except Exception as exception:
        logger.exception("Error deleting category")
        return AppServices.handle_exception(exception)


@category_router.get("/get/{id}")
async def get_category_by_id_controller(id: int):
    try:
        logger.info("Fetching category details for ID: %d", id)
        response_payload = CategoryService.get_category_by_id_service(id)

        if not response_payload:
            logger.warning("Category not found: ID %d", id)
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )
        logger.info("Category retrieved: %s", response_payload.category_name)
        return AppServices.app_response(
            HttpStatusCodeEnum.OK.value,
            ResponseMessageEnum.GET_DATA.value,
            success=True,
            data=response_payload,
        )

    except Exception as exception:
        logger.exception("Error fetching category details")
        return AppServices.handle_exception(exception)


@category_router.put("/update/{id}")
async def update_category_controller(update_category_dto: UpdateCategoryDTO):
    try:

        response_payload = CategoryService.update_category_service(
            update_category_dto)
        if not response_payload:
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )
        # logger.info("Attempting to update category: ID %d, Name: %s", id,
        #             update_category_dto.category_name)
        return AppServices.app_response(
            HttpStatusCodeEnum.OK.value,
            ResponseMessageEnum.UPDATE_DATA.value,
            success=True,
            data=response_payload,
        )
    except Exception as exception:
        logger.exception("Error updating category")
        return AppServices.handle_exception(exception)
