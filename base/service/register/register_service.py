import bcrypt
from fastapi import FastAPI

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.static_enum import StaticVariables
from base.dao.login.login_dao import LoginDAO
from base.dao.register.register_dao import RegisterDAO
from base.utils.custom_exception import AppServices
from base.utils.time_stamp import get_current_timestamp
from base.vo.login_vo import LoginVO
from base.vo.register_vo import RegisterVO
from base.vo.role_vo import RoleVO

logger = get_logger()
app = FastAPI()


class RegisterService:
    @staticmethod
    def register_user(register_dto):
        """Handles user registration logic."""

        existing_user = RegisterDAO.check_existing_user(
            register_dto.register_username)
        if existing_user:
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.ALREADY_EXISTS,
                success=False, data={}
            )

        # Hash password
        hashed_password = bcrypt.hashpw(
            register_dto.register_password.encode(), bcrypt.gensalt()).decode()

        timestamp = get_current_timestamp()

        # Create and insert login user
        login_user = LoginVO(
            login_username=register_dto.register_username,
            login_password=hashed_password,
            created_at=timestamp,
            modified_at=timestamp
        )

        login_record = LoginDAO.insert_login_user(login_user)
        if not login_record:
            return AppServices.app_response(
                HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
                ResponseMessageEnum.USER_LOGIN_FAILED,
                success=False, data={}
            )

        role_record = RegisterDAO.get_role(
            RoleVO(role_name=StaticVariables.ADMIN_ROLE))
        print("role_record>>>>>>>>>>>>>>>>>>>>>>>>>>", role_record)
        logger.info(f"Role Record: {role_record}, Type: {type(role_record)}")

        if not role_record:
            return AppServices.app_response(
                HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
                ResponseMessageEnum.USER_NOT_FOUND,
                success=False, data={}
            )

        # Create and insert registered user
        register_user = RegisterVO(
            register_login_vo=login_record.id,
            register_firstname=register_dto.register_firstname,
            register_lastname=register_dto.register_lastname,
            register_email=register_dto.register_email,
            register_gender=register_dto.register_gender,
            register_phone=register_dto.register_phone,
            role=role_record.id,
            created_at=timestamp,
            modified_at=timestamp
        )
        print("register_user>>>>>>>>>>>>>>>>>>>>>>>>>>", register_user.role)

        register_record = RegisterDAO.insert_register_user(register_user)
        if not register_record:
            return AppServices.app_response(
                HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
                ResponseMessageEnum.NOT_FOUND,
                success=False, data={}
            )

        return AppServices.app_response(
            HttpStatusCodeEnum.CREATED,
            ResponseMessageEnum.INSERT_DATA,
            success=True,
            data={register_record}
        )
