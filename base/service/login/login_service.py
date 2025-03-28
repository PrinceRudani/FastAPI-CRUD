from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.login.login_dao import LoginDAO
from base.utils.custom_exception import AppServices


class LoginService:
    @staticmethod
    def login_username_password_check(login_details):
        """Login username and password."""
        validate_login_id = LoginDAO.get_login_id(login_details)
        if not validate_login_id:
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.USER_LOGIN_FAILED,
                success=False,
                data={},
            )
        return validate_login_id

    @staticmethod
    def successful_login_user(login_data, password):
        """Login successful."""
        if login_data.is_deleted:
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.USER_LOGIN_FAILED,
                success=False,
                data={"message": "Login failed"},
            )
        if password != login_data.login_password:
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.USER_LOGIN_FAILED,
                success=False,
                data={"message": "wrong password"},
            )
        if password == login_data.login_password:
            return AppServices.app_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.USER_LOGIN_SUCCESS,
                success=True,
                data={"message": "Login successful"},
            )
        else:
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.USER_LOGIN_FAILED,
                success=False,
                data={"message": "Wrong password or username"},
            )

    @staticmethod
    def insert_login_user_service(login_dto):
        """Login user."""
        username = login_dto.login_username
        password = login_dto.login_password
        login_validate_data = LoginService.login_username_password_check(username)
        if login_validate_data is None:
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.USER_LOGIN_FAILED,
                success=False,
                data={"message": "Login failed"},
            )
        return LoginService.successful_login_user(login_validate_data, password)
