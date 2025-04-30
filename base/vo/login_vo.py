from sqlalchemy import Column, Integer, String, Boolean

from base.db.database import Base, Database

# database = Database()
# engine = database.get_db_connection()


class LoginVO(Base):
    __tablename__ = "login_table"

    id = Column(Integer, primary_key=True, index=True)
    login_username = Column(String(50), unique=True, index=True, nullable=False)
    login_password = Column(String(100))
    login_status = Column(Boolean, default=False)
    created_at = Column(String(30))
    modified_at = Column(String(30))


# Base.metadata.create_all(engine)
