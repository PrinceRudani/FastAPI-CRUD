from sqlalchemy import Column, Integer, String, Boolean

from base.db.database import Base


class CategoryVO(Base):
    __tablename__ = "category_table"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), unique=True, index=True)
    category_description = Column(String(100))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(Integer, nullable=False)
    modified_at = Column(Integer, nullable=False)
