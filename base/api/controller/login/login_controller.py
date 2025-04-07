from fastapi import APIRouter, HTTPException, Response, BackgroundTasks

from base.api.controller.notification.notification_controller import (
    NotificationController,
)
from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.login.login_dto import LoginDTO
from base.service.login.login_service import LoginService
from base.utils.custom_exception import AppServices

logger = get_logger()

login_router = APIRouter(
    prefix="/login",
    tags=["Login"],
    responses={404: {"description": "API endpoint not found"}},
)


@login_router.post("/user_login")
def user_login(
    login_dto: LoginDTO,
    response: Response,
    background_tasks: BackgroundTasks,
):
    try:
        if not login_dto:
            raise HTTPException(status_code=400, detail="Invalid login request.")

        response_payload = LoginService.login_user(
            login_dto, response, background_tasks
        )

        return response_payload

    except Exception as ex:
        logger.error(f"Login Error: {str(ex)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@login_router.post("/user_logout")
def user_logout(login_dto: LoginDTO, response: Response):
    try:
        if not login_dto:
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )

        response_payload = LoginService.logout_user(login_dto, response)

        return response_payload

    except Exception as ex:
        logger.error(f"Logout Error: {str(ex)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
