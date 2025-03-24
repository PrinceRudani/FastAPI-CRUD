from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from base.db.database import Base, engine


class SubcategoryVO(Base):
    __tablename__ = "subcategory_table"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer,
                         ForeignKey('category_table.id', ondelete="CASCADE",
                                    onupdate="CASCADE"), nullable=False)

    subcategory_name = Column(String(50), unique=True, index=True)
    subcategory_description = Column(String(100))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(Integer, nullable=False)
    modified_at = Column(Integer, nullable=False)

    # Correct relationship
    category = relationship("CategoryVO", back_populates="subcategories")


Base.metadata.create_all(bind=engine)
print("Table created successfully!")
