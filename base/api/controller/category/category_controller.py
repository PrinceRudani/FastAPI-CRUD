from fastapi import APIRouter, Request, Response, Depends, BackgroundTasks

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.category.category_dto import CategoryDTO, UpdateCategoryDTO
from base.middleware.api_key_validator import verify_api_key
from base.service.category.category_service import CategoryService
from base.service.login.login_service import login_required
from base.utils.custom_exception import AppServices

logger = get_logger()

category_router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "API endpoint not found"}},
)


@category_router.post("/insert", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def insert_category_controller(
    request: Request,
    response: Response,
    category_dto: CategoryDTO,
    background_tasks: BackgroundTasks,
):
    try:
        if not category_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )
        logger.info("Attempting to insert new category: %s", category_dto.category_name)
        result = CategoryService.insert_category_service(category_dto, background_tasks)

        return result

    except Exception as exception:
        logger.exception("Error inserting category")
        return AppServices.handle_exception(exception)


@category_router.get("/all", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def view_category_controller(request: Request, response: Response):
    try:
        response_payload = CategoryService.get_all_categories_service()
        logger.info(f"Response for verify_member is {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching categories")
        return AppServices.handle_exception(exception)


@category_router.delete("/delete/{id}", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def delete_category_controller(
    request: Request,
    response: Response,
    id,
    background_tasks: BackgroundTasks,
):
    try:
        response_payload = CategoryService.delete_category_service(id, background_tasks)
        print("respomse>>>>>>>>>>>", response_payload)

        logger.info(f"Response for verify_member is {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting category")
        return AppServices.handle_exception(exception)


@category_router.get("/get/{id}", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def get_category_by_id_controller(
    request: Request, response: Response, id: int, background_tasks: BackgroundTasks
):
    print(">>>>>>>>>>>>>")
    try:
        logger.info("Fetching category details for ID: %d", id)
        response_payload = CategoryService.get_category_by_id_service(
            id, background_tasks
        )

        logger.info("Response for fetching category")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching category details")
        return AppServices.handle_exception(exception)


@category_router.put("/update/{id}", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def update_category_controller(
    request: Request,
    response: Response,
    update_category_dto: UpdateCategoryDTO,
    background_tasks: BackgroundTasks,
):
    try:
        response_payload = CategoryService.update_category_service(
            update_category_dto, background_tasks
        )

        logger.info("Response for update_category is %s", response_payload)
        return response_payload
    except Exception as exception:
        logger.exception("Error updating category")
        return AppServices.handle_exception(exception)
