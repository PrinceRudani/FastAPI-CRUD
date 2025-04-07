import logging

from fastapi import APIRouter, Response, Request, Depends

from base.api.controller.notification.notification_controller import \
    NotificationController
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.subcategory.subcategory_dto import SubcategoryDTO, \
    UpdateSubcategoryDTO
from base.middleware.api_key_validator import verify_api_key
from base.service.login.login_service import login_required
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


@subcategory_router.post("/insert", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def insert_subcategory_controller(request: Request, response: Response,
                                  subcategory_dto:
                                  SubcategoryDTO):
    try:
        if not subcategory_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )
        email_sent = NotificationController.send_email_notification(
            to_email=StaticVariables.RECEIVER_EMAIL,
            subject=" Subcategory updated successfully",
            message=f"Subcategory '{subcategory_dto.subcategory_name}' was successfully "
                    f"updated."
        )
        logger.info("Inserting new subcategory: %s",
                    subcategory_dto.subcategory_name)
        result = SubcategoryService.insert_subcategory_service(subcategory_dto)
        return result, email_sent

    except Exception as e:
        logger.error("Error inserting subcategory: %s", str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.get("/all", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def view_subcategory_controller(request: Request, response: Response):
    try:
        logger.info("Fetching all subcategories")
        response_payload = SubcategoryService.get_all_subcategories_service()

        return response_payload
    except Exception as e:
        logger.error("Error fetching subcategories: %s", str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.delete("/delete/{id}",
                           dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def delete_subcategory_controller(request: Request, response: Response,
                                  id: int):
    try:
        logger.info("Deleting subcategory with ID: %d", id)
        response_payload = SubcategoryService.delete_subcategory_service(id)
        email_sent = NotificationController.send_email_notification(
            to_email=StaticVariables.RECEIVER_EMAIL,
            subject=" Subcategory deleted successfully",
            message=f"Subcategory '{id}' was successfully deleted."
        )
        return response_payload, email_sent
    except Exception as e:
        logger.error("Error deleting subcategory with ID %d: %s", id, str(e))
        raise AppServices.handle_exception(e, is_raise=True)


@subcategory_router.get("/get/{id}", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def get_subcategory_by_id_controller(request: Request, response: Response,
                                     id: (int)):
    try:
        logger.info("Fetching subcategory with ID: %d", id)
        response_payload = SubcategoryService.get_subcategory_by_id_service(id)
        email_sent = NotificationController.send_email_notification(
            to_email=StaticVariables.RECEIVER_EMAIL,
            subject=" Subcategory fetched successfully",
            message=f"Subcategory '{id}' was successfully fetched."
        )
        return response_payload, email_sent
    except Exception as exception:
        logger.error("Error fetching subcategory with ID %d: %s", id,
                     str(exception))
        raise AppServices.handle_exception(exception, is_raise=True)


@subcategory_router.put("/update/{id}", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def update_subcategory_controller(request: Request, response: Response,
                                  update_subcategory_dto: UpdateSubcategoryDTO):
    try:
        logger.info("Updating subcategory with ID")
        response_payload = SubcategoryService.update_subcategory_service(
            update_subcategory_dto
        )
        email_sent = NotificationController.send_email_notification(
            to_email=StaticVariables.RECEIVER_EMAIL,
            subject=" Subcategory update successfully",
            message=f"Subcategory '{id}' was successfully update."
        )
        return response_payload, email_sent
    except Exception as e:
        logger.error("Error updating subcategory with ")
        raise AppServices.handle_exception(e, is_raise=True)
