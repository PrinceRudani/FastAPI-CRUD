from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from base.db.database import Base


# database = Database()
# engine = database.get_db_connection()


class RegisterVO(Base):
    __tablename__ = "register_table"

    id = Column(Integer, primary_key=True, index=True)
    register_login_vo = Column(
        Integer,
        ForeignKey("login_table.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    register_firstname = Column(String(50), nullable=False)
    register_lastname = Column(String(50), nullable=False)
    register_email = Column(String(50), nullable=False)
    register_gender = Column(String(50), nullable=False)
    register_phone = Column(String(50), nullable=False)
    is_delete = Column(Boolean, nullable=False, default=False)
    created_at = Column(String(30))
    modified_at = Column(String(30))


# Base.metadata.create_all(engine)
