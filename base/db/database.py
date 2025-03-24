from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from base.utils.custom_exception import AppServices
from config import settings

POOL_SIZE = 10
POOL_RECYCLE = 3600
POOL_TIMEOUT = 15
MAX_OVERFLOW = 0
CONNECTION_TIMEOUT = 60

DATABASE_URL = settings.DATABASE_URL

# Initialize engine globally
engine = create_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    pool_recycle=POOL_RECYCLE,
    pool_timeout=POOL_TIMEOUT,
    max_overflow=MAX_OVERFLOW,
    connect_args={"connect_timeout": CONNECTION_TIMEOUT},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Define Base for ORM models
Base = declarative_base()


class Database:
    _instance = None

    def __new__(cls):
        """Singleton implementation for Database class."""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection_is_active = False
            cls._instance.engine = None
        return cls._instance

    def get_db_connection(self):
        """Establishes and returns a database engine connection."""
        if not self.connection_is_active:
            try:
                self.engine = engine  # Use the pre-initialized engine
                self.connection_is_active = True
                print("Database connection established:", self.engine)
                return self.engine
            except Exception as e:
                print("Database connection failed:", e)
                AppServices.handle_exception(e, is_raise=True)
        return self.engine

    @staticmethod
    def get_db_session():
        """Provides a new database session."""
        try:
            db_session = SessionLocal()
            return db_session
        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)
