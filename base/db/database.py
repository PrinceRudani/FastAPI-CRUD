"""
This module provides database connectivity and session management.

Author: Tarun Mondal
Designation: Software Engineer
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from base.utils.constant import settings
from base.utils.custom_exception import AppServices

DB_HOST = settings.DB_HOST
DB_USERNAME = settings.DB_USERNAME
DB_PASSWORD = settings.DB_PASSWORD
DB_PORT = settings.DB_PORT
DB_NAME = settings.DB_NAME

MYSQL_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
POOL_SIZE = 10
POOL_RECYCLE = 3600
POOL_TIMEOUT = 15
MAX_OVERFLOW = 0
CONNECT_TIMEOUT = 3600
PREPING = True


class Database:
    """
    Singleton class for managing database connections and sessions.
    Author: Tarun Mondal
    Designation: Software Engineer
    """

    _instance = None

    def __init__(self):
        self.engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection_is_active = False
            cls._instance.engine = None
        return cls._instance

    def get_db_connection(self):
        """
        Get a database engine connection.
        Author: Tarun Mondal
        Designation: Software Engineer

        Returns:
            engine: SQLAlchemy database engine.
        """
        if not self.connection_is_active:
            connect_args = {"connect_timeout": CONNECT_TIMEOUT}
            try:
                self.engine = create_engine(
                    MYSQL_URL,
                    pool_size=POOL_SIZE,
                    pool_recycle=POOL_RECYCLE,
                    pool_timeout=POOL_TIMEOUT,
                    max_overflow=MAX_OVERFLOW,
                    connect_args=connect_args,
                    pool_pre_ping=PREPING,
                )
                print("Database connection established : ", self.engine)
                return self.engine
            except Exception as exception:
                AppServices.handle_exception(exception, is_raise=True)
        return self.engine

    @staticmethod
    def get_db_session(engine):
        """
        Get a database session.
        Author: Tarun Mondal
        Designation: Software Engineer

        Args:
            engine: SQLAlchemy database engine.

        Returns:
            session: SQLAlchemy database session.
        """
        try:
            db_session = sessionmaker(bind=engine)
            session = db_session()
            return session
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)


Base = declarative_base()
database = Database()
engine = database.get_db_connection()
Base.metadata.create_all(engine)
