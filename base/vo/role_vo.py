from sqlalchemy import Column, String, Integer, Boolean
from base.db.database import Base  # Import shared Base (don't redefine it)


class RoleVO(Base):
    __tablename__ = "role_table"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_on = Column(String(30), nullable=False)
    modified_on = Column(String(30), nullable=False)
