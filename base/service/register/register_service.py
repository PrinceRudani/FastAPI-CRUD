# from base.config.logger_config import get_logger
# from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
# from base.dao.login.login_dao import LoginDAO  # Import LoginDAO
# from base.dao.register.register_dao import RegisterDAO
# from base.utils.custom_exception import AppServices
# from base.utils.time_stamp import get_current_timestamp
# from base.vo.login_vo import LoginVO
# from base.vo.register_vo import RegisterVO
#
# logger = get_logger()
#
#
# class RegisterService:
#     @staticmethod
#     def insert_register_service(register_dao_data):
#         """Convert DTO to Model & Insert Register with Login."""
#         try:
#
#
#             login_vo = LoginVO()
#             login_vo.login_username = register_dao_data.login_username
#             login_vo.login_password = register_dao_data.login_password
#             login_insert_data = LoginDAO.insert_login_dao(login_vo)
#             login_id = login_insert_data.id
#
#             register_vo = RegisterVO()
#             register_vo.register_login_vo = login_id
#             register_vo.register_firstname = register_dao_data.register_firstname
#             register_vo.register_lastname = register_dao_data.register_lastname
#             register_vo.register_email = register_dao_data.register_email
#             register_vo.register_gender = register_dao_data.register_gender
#             register_vo.register_phone = register_dao_data.register_phone
#             register_vo.created_at = get_current_timestamp()
#             register_vo.modified_at = get_current_timestamp()
#
#             register_insert_data = RegisterDAO.insert_register_dao(register_vo)
#             if not register_insert_data:
#                 return AppServices.app_response(
#                     HttpStatusCodeEnum.BAD_REQUEST.value,
#                     "Failed to insert register details",
#                     success=False, data={}
#                 )
#
#             logger.info("Register inserted successfully: %s",
#                         register_vo.register_firstname)
#             return AppServices.app_response(
#                 HttpStatusCodeEnum.CREATED.value,
#                 ResponseMessageEnum.INSERT_DATA.value,
#                 success=True,
#                 data={"register_id": register_insert_data.id,
#                       "login_id": login_id},
#             )
#
#         except Exception as exception:
#             logger.exception("Error inserting register")
#             return AppServices.handle_exception(exception)
#
#
# @app.post("/register")
# def register(register_dto):
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")
#     hashed_password = hash_password(user.password)
#     new_user = User(username=user.username, password=hashed_password,
#                     first_name=user.first_name, last_name=user.last_name,
#                     email=user.email, phone=user.phone)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User registered successfully"}
