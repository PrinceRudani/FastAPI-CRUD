from fastapi import APIRouter, HTTPException, Response

from base.config.logger_config import get_logger
from base.dto.login.login_dto import LoginDTO
from base.service.login.login_service import LoginService

logger = get_logger()

login_router = APIRouter(
    prefix="/login",
    tags=["Login"],
    responses={404: {"description": "API endpoint not found"}},
)


@login_router.post("/user_login")
def user_login(login_dto: LoginDTO, response: Response):
    try:
        if not login_dto:
            raise HTTPException(status_code=400, detail="Invalid login request.")

        response_payload = LoginService.insert_login_user_service(login_dto)
        return response_payload

    except Exception as ex:
        logger.error(f"Login Error: {str(ex)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
