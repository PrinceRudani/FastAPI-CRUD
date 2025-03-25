from sqlalchemy import Column, Integer, String, Boolean

from base.db.database import Base, Database

database = Database()
engine = database.get_db_connection()

class CategoryVO(Base):
    __tablename__ = "category_table"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), unique=True, index=True, nullable=False)
    category_description = Column(String(100))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(String(30))
    modified_at = Column(String(30))

Base.metadata.create_all(engine)
