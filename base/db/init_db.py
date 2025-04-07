from sqlalchemy.orm import declarative_base

from base.db.database import Database, Base
from base.vo.category_vo import CategoryVO
from base.vo.subcategory_vo import SubcategoryVO
from base.vo.product_vo import ProductVO
from base.vo.role_vo import RoleVO
from base.vo.register_vo import RegisterVO  # Import models in order

# Initialize database connection
Base = declarative_base()
database = Database()
engine = database.get_db_connection()
Base.metadata.create_all(engine)


print("✅ Database tables created successfully.")
