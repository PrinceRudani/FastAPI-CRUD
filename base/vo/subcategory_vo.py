from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from base.db.database import Base, Database

database = Database()
engine = database.get_db_connection()


class SubcategoryVO(Base):
    __tablename__ = "subcategory_table"

    id = Column(Integer, primary_key=True, index=True)
    subcategory_category_id = Column(
        Integer,
        ForeignKey("category_table.id", ondelete="CASCADE",
                   onupdate="CASCADE"), nullable=False,
    )
    print(subcategory_category_id)
    subcategory_name = Column(String(50), unique=True, index=True,
                              nullable=False)
    subcategory_description = Column(String(100))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(String(30))
    modified_at = Column(String(30))


Base.metadata.create_all(engine)
