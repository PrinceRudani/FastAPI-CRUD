from fastapi import APIRouter, Response

from base.api.controller.notification.notification_controller import \
    NotificationController
from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.register.register_dto import RegisterDTO
from base.service.register.register_service import RegisterService
from base.utils.custom_exception import AppServices

logger = get_logger()

register_router = APIRouter(
    prefix="/register",
    tags=["Register"],
    responses={404: {"description": "API endpoint not found"}},
)


@register_router.post("/register")
def insert_register_controller(register_dto: RegisterDTO,
                               response: Response):
    try:
        if not register_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )
        email_sent = NotificationController.send_email_notification(
            to_email=StaticVariables.RECEIVER_EMAIL,
            subject=" user register successfully",
            message=f"user register"
                    f" {register_dto.register_firstname + register_dto.register_lastname}'successfully ."
        )

        result = RegisterService.register_user(register_dto)
        return result, email_sent

    except Exception as exception:
        logger.exception("Error inserting register")
        return AppServices.handle_exception(exception)
