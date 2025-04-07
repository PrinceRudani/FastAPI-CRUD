from datetime import datetime, timedelta
from functools import wraps

import bcrypt
import jwt
from fastapi import HTTPException, Response, status, Request
from passlib.context import CryptContext

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.static_enum import StaticVariables
from base.dao.login.login_dao import LoginDAO
from base.utils.custom_exception import AppServices

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = get_logger()

from base.utils.constant import Constant

print("Access Token Expiry Time:", Constant.ACCESS_TOKEN_EXP)


class LoginService:

    @staticmethod
    def generate_tokens(user_id, username, user_role):
        print("Access Token Expiry Time:", Constant.ACCESS_TOKEN_EXP)
        access_token_expiry = timedelta(seconds=Constant.ACCESS_TOKEN_EXP)
        refresh_token_expiry = timedelta(seconds=Constant.REFRESH_TOKEN_EXP)
        print("Refresh Token Expiry:", refresh_token_expiry)
        print("Access Token Expiry:", access_token_expiry)

        access_token = jwt.encode(
            {
                "user_id": user_id,
                "username": username,
                "user_role": user_role,
                "exp": datetime.utcnow() + access_token_expiry
            },
            Constant.SECRET_KEY,
            algorithm=Constant.HASH_ALGORITHM
        )

        refresh_token = jwt.encode(
            {
                "user_id": user_id,
                "username": username,
                "user_role": user_role,  # 🔥 Add this line
                "exp": datetime.utcnow() + refresh_token_expiry
            },
            Constant.SECRET_KEY,
            algorithm=Constant.HASH_ALGORITHM
        )
        print(f"access_token={access_token}")
        print(f"refresh_token={refresh_token}")
        return access_token, refresh_token

    @staticmethod
    def login_user(login_dto, response: Response):
        user = LoginDAO.get_user_by_username(login_dto.login_username)
        print(">>>>user", user)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User not found")

        if not bcrypt.checkpw(login_dto.login_password.encode(),
                              user.login_password.encode()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username or password")

        user.login_status = True
        LoginDAO.update_login_status(user)

        username = user.login_username
        user_role = StaticVariables.ADMIN_ROLE
        print(f"username={username}, user_role={user_role}, user_id={user.id}")

        access_token, refresh_token = LoginService.generate_tokens(user.id,
                                                                   username,
                                                                   user_role)

        response.set_cookie("access_token", access_token,
                            max_age=Constant.ACCESS_TOKEN_EXP,
                            httponly=True)
        response.set_cookie("refresh_token", refresh_token,
                            max_age=Constant.REFRESH_TOKEN_EXP, httponly=True)

        return {"message": "Login successful", "access_token": access_token,
                "refresh_token": refresh_token}

    @staticmethod
    def refresh_token(response: Response, request):
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Refresh token missing")

        try:
            data = jwt.decode(refresh_token, Constant.SECRET_KEY,
                              algorithms=[Constant.HASH_ALGORITHM])

            access_token, new_refresh_token = LoginService.generate_tokens(
                data["user_id"], data["username"],
                user_role=StaticVariables.ADMIN_ROLE)

            response.set_cookie("access_token", access_token,
                                max_age=Constant.ACCESS_TOKEN_EXP,
                                httponly=True)
            response.set_cookie("refresh_token", new_refresh_token,
                                max_age=Constant.REFRESH_TOKEN_EXP,
                                httponly=True)

            return {"message": "Tokens refreshed successfully",
                    "access_token": access_token,
                    "refresh_token": new_refresh_token}

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Refresh token expired")
        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid refresh token")

    @staticmethod
    def logout_user(login_dto, response: Response):
        user = LoginDAO.get_user_by_username(login_dto.login_username)
        if user.login_status is False:
            return AppServices.app_response(HttpStatusCodeEnum.BAD_REQUEST,
                                            ResponseMessageEnum.NOT_FOUND,
                                            success=False,
                                            data={"message": "User already "
                                                             "logged out"})

        if not user:
            return AppServices.app_response(HttpStatusCodeEnum.NOT_FOUND,
                                            ResponseMessageEnum.NOT_FOUND,
                                            success=False,
                                            data={"message": "User not found"})

        user.login_status = False
        LoginDAO.update_login_status(user)

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return {"message": "Logout successful"}


def login_required(required_roles=None):
    if required_roles is None:
        required_roles = []

    def decorator(route_function):
        @wraps(route_function)
        def wrapper(request: Request, response: Response, *args,
                    **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                token = request.cookies.get("access_token")

            try:
                token = token.replace("Bearer ", "")
                decoded_data = jwt.decode(token, Constant.SECRET_KEY,
                                          algorithms=[Constant.HASH_ALGORITHM])

                user_id = decoded_data.get("user_id")
                user_role = decoded_data.get("user_role")

                if not user_id or not user_role:
                    raise HTTPException(status_code=401,
                                        detail="Invalid token: Missing user_id or user_role")

                if required_roles and user_role not in required_roles:
                    raise HTTPException(status_code=403,
                                        detail=f"Insufficient permissions: Required roles {required_roles}, found {user_role}")

                return route_function(request, response, *args, **kwargs)

            except jwt.ExpiredSignatureError:
                # 🔥 Access token expired, try to refresh it
                refresh_token = request.cookies.get("refresh_token")
                if not refresh_token:
                    raise HTTPException(status_code=401,
                                        detail="Refresh token missing. Please log in again.")

                try:
                    decoded_refresh_token = jwt.decode(refresh_token,
                                                       Constant.SECRET_KEY,
                                                       algorithms=[
                                                           Constant.HASH_ALGORITHM])

                    # Generate new access & refresh tokens
                    access_token, new_refresh_token = LoginService.generate_tokens(
                        decoded_refresh_token["user_id"],
                        decoded_refresh_token["username"],
                        decoded_refresh_token["user_role"]
                    )

                    # Set new tokens in cookies
                    response.set_cookie("access_token", access_token,
                                        max_age=Constant.ACCESS_TOKEN_EXP,
                                        httponly=True)
                    response.set_cookie("refresh_token", new_refresh_token,
                                        max_age=Constant.REFRESH_TOKEN_EXP,
                                        httponly=True)

                    return route_function(request, response, *args, **kwargs)

                except jwt.ExpiredSignatureError:
                    raise HTTPException(status_code=401,
                                        detail="Refresh token expired. Please log in again.")
                except jwt.DecodeError:
                    raise HTTPException(status_code=401,
                                        detail="Invalid refresh token.")

            except jwt.DecodeError:
                raise HTTPException(status_code=401,
                                    detail="Invalid token format.")

        return wrapper

    return decorator
