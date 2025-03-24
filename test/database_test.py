# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# from base.utils.custom_exception import AppServices
# from config import settings
#
# POOL_SIZE = 10
# POOL_RECYCLE = 3600
# POOL_TIMEOUT = 15
# MAX_OVERFLOW = 0
# CONNECTION_TIMEOUT = 60
# PREPING = True
#
# DATABASE_URL = settings.DATABASE_URL
#
# engine = create_engine(DATABASE_URL)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# """Base is a superclass for all ORM models.
# All database models (tables) will inherit from Base."""
#
#
#
# class Database:
#     _instance = None
#
#     def __init__(self):
#         self.engine = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(Database).__new__(cls)
#             cls._instance.connection_is_active = False
#             cls._instance.engine = None
#         return cls._instance
#
#     @staticmethod
#     def get_db_connection(self):
#         if not self.connection_is_active:
#             connection_args = {"connection_timeout": CONNECTION_TIMEOUT}
#             try:
#                 self.engine = create_engine(
#                     DATABASE_URL,
#                     pool_size=POOL_SIZE,
#                     pool_recycle=POOL_RECYCLE,
#                     pool_timeout=POOL_TIMEOUT,
#                     max_overflow=MAX_OVERFLOW,
#                     connect_args=connection_args,
#                     pool_pre_ping=True
#                 )
#                 print("Database connection established :", self.engine)
#                 return self.engine
#             except Exception as e:
#                 print("Database connection failed :", self.engine)
#                 AppServices.handle_exception(e, is_raise=True)
#         return self.engine
#
#     @staticmethod
#     def get_db_session(engine):
#         try:
#             db_session = sessionmaker(bind=engine)
#             session = db_session()
#             return session
#         except Exception as exception:
#             return AppServices.handle_exception(exception, is_raise=True)



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/FastCRUD_db"
#
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
# """Base is a superclass for all ORM models.
# All database models (tables) will inherit from Base."""
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()