from sqlalchemy.orm import Session

from base.dao.category.category_dao import CategoryDAO
from base.dto.category.category_dto import CategoryDTO
from base.utils.time_stamp import get_current_timestamp
from base.vo.category_vo import CategoryVO
from base.config.logger_config import get_logger

logger = get_logger()


class CategoryService:
    @staticmethod
    def insert_category(category_dto: CategoryDTO, session: Session):
        """Convert DTO to Model & Insert Category."""
        db_category = CategoryVO(**category_dto.model_dump())
        db_category.created_at = get_current_timestamp()
        db_category.modified_at = get_current_timestamp()
        return CategoryDAO.insert_category(session, db_category)

    @staticmethod
    def get_all_categories(session: Session):
        """Fetch all categories using CategoryDAO."""
        return CategoryDAO.get_all_categories(session)

    @staticmethod
    def delete_category(session: Session, id: int):
        """Soft delete a category by ID."""
        return CategoryDAO.delete_category(session, id)

    @staticmethod
    def get_category_by_id(session: Session, id: int):
        """Retrieve category details for editing."""
        category = CategoryDAO.get_category_by_id(session, id)

        if not category:
            raise ValueError("Category not found")

        return category

    @staticmethod
    def update_category(session: Session, id: int, category_dto: CategoryDTO):
        """Update category details."""
        category = CategoryDAO.get_category_by_id(session, id)

        if not category:
            raise ValueError("Category not found")

        # Update category fields
        category.category_name = category_dto.category_name
        category.category_description = category_dto.category_description
        category.modified_at = get_current_timestamp()

        return CategoryDAO.update_category(session, category)
