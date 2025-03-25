from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from base.db.database import Base
from base.vo.category_vo import CategoryVO


class SubcategoryVO(Base):
    __tablename__ = "subcategory_table"

    id = Column(Integer, primary_key=True, index=True)
    subcategory_category_id = Column(
        Integer,
        ForeignKey(CategoryVO.id, ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    subcategory_name = Column(String(50), unique=True, index=True, nullable=False)
    subcategory_description = Column(String(100))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(String(30))
    modified_at = Column(String(30))
