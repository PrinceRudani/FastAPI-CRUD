from base.config.logger_config import get_logger
from base.dao.category.category_dao import CategoryDAO
from base.utils.custom_exception import AppServices
from base.utils.time_stamp import get_current_timestamp
from base.vo.category_vo import CategoryVO

logger = get_logger()


class CategoryService:
    @staticmethod
    def insert_category_service(category_dao_data):
        """Convert DTO to Model & Insert Category."""
        try:
            category_vo = CategoryVO()
            category_vo.category_name = category_dao_data.category_name
            category_vo.category_description = category_dao_data.category_description
            category_vo.created_at = get_current_timestamp()
            category_vo.modified_at = get_current_timestamp()
            category_insert_data = CategoryDAO.insert_category_dao(category_vo)

            logger.info("Category inserted successfully: %s",
                        category_vo.category_name)
            return category_insert_data

        except Exception as exception:
            logger.exception("Error inserting category")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_all_categories_service():
        """Fetch all categories using CategoryDAO."""
        try:
            get_all_category_data = CategoryDAO.get_all_categories_dao()
            return get_all_category_data
        except Exception as exception:
            logger.exception("Error fetching all categories")
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_category_service(id: int):
        """Soft delete a category by ID."""
        try:
            delete_dao_data = CategoryDAO.delete_category_dao(id)
            delete_dao_data.is_deleted = True
            return delete_dao_data

        except Exception as exception:
            logger.exception("Error deleting category")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_category_by_id_service(id: int):
        """Retrieve category details for editing."""
        try:
            category = CategoryDAO.get_category_by_id_dao(id)
            return category
        except Exception as exception:
            logger.exception("Error retrieving category with ID %d", id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_category_service(category_data):
        """Update category details."""
        try:

            category_vo = CategoryVO()
            category_vo.category_name = category_data.category_name
            category_vo.category_description = category_data.category_description

            category_vo.modified_at = get_current_timestamp()
            updated_category = CategoryDAO.update_category_dao(category_vo)
            return updated_category

        except Exception as exception:
            logger.exception("Error updating category with ID %d", id)
            return AppServices.handle_exception(exception)
