# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
#
# class Settings:
#     DB_SCHEME = os.getenv("DB_SCHEME")
#     DB_USER = os.getenv("DB_USER")
#     DB_PASSWORD = os.getenv("DB_PASSWORD")
#     DB_HOST = os.getenv("DB_HOST")
#     DB_PORT = os.getenv("DB_PORT")
#     DB_NAME = os.getenv("DB_NAME")
#
#     DATABASE_URL = (
#         f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     )
#
#     ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
#     REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
#     ACCESS_TOKEN_EXP = int(os.getenv("ACCESS_TOKEN_EXP"))
#     REFRESH_TOKEN_EXP = int(os.getenv("REFRESH_TOKEN_EXP"))
#     TIME_OUT_MAX_AGE = int(os.getenv("TIME_OUT_MAX_AGE"))
#
#     ENCODING = os.getenv("ENCODING")
#     HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
#     JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
#
#     ROLE_ADMIN = os.getenv("ROLE_ADMIN")
#     ROLE_USER = os.getenv("ROLE_USER")
#
#
# settings = Settings()
