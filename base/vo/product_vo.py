from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import JSON

from base.db.database import Base, Database

# database = Database()
# engine = database.get_db_connection()


class ProductVO(Base):
    __tablename__ = "product_table"

    id = Column(Integer, primary_key=True, index=True)
    product_category_id = Column(
        Integer,
        ForeignKey("category_table.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    product_subcategory_id = Column(
        Integer,
        ForeignKey("subcategory_table.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    product_name = Column(String(50), unique=True, index=True, nullable=False)
    product_description = Column(String(255))

    product_price = Column(Integer, default=0, nullable=False)
    product_image_names = Column(JSON, nullable=True)
    product_image_paths = Column(JSON, nullable=True)
    product_quantity = Column(Integer, default=0)

    is_deleted = Column(Boolean, default=False)
    created_at = Column(String(30))
    modified_at = Column(String(30))


# Base.metadata.create_all(engine)
