from base.config.logger_config import get_logger
from base.custom_enum.http_enum import ResponseMessageEnum, HttpStatusCodeEnum
from base.dao.category.category_dao import CategoryDAO
from base.dto.category.category_dto import CategoryDTO
from base.utils.custom_exception import AppServices
from base.utils.time_stamp import get_current_timestamp
from base.vo.category_vo import CategoryVO

logger = get_logger()

class CategoryService:
    @staticmethod
    def insert_category_service(category_dto: CategoryDTO, session):
        """Convert DTO to Model & Insert Category."""
        try:
            if not category_dto:
                logger.warning("Attempt to insert an empty category DTO")
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )

            category_vo = CategoryVO(**category_dto.model_dump())
            category_vo.created_at = get_current_timestamp()
            category_vo.modified_at = get_current_timestamp()
            result = CategoryDAO.insert_category_dao(category_vo, session)

            logger.info("Category inserted successfully: %s", category_vo.category_name)
            return AppServices.app_response(
                HttpStatusCodeEnum.CREATED.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=result,
            )
        except Exception as exception:
            logger.exception("Error inserting category")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_all_categories_service(session):
        """Fetch all categories using CategoryDAO."""
        try:
            categories = CategoryDAO.get_all_categories_dao(session)
            logger.info("Fetched %d categories", len(categories))
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=categories,
            )
        except Exception as exception:
            logger.exception("Error fetching categories")
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_category_service(id: int, session):
        """Soft delete a category by ID."""
        try:
            result = CategoryDAO.delete_category_dao(session, id)
            logger.info("Category deleted: ID %d", id)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=result,
            )
        except Exception as exception:
            logger.exception("Error deleting category with ID %d", id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_category_by_id_service(id: int, session):
        """Retrieve category details for editing."""
        try:
            category = CategoryDAO.get_category_by_id_dao(session, id)
            if not category:
                logger.warning("Category not found: ID %d", id)
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )
            logger.info("Category retrieved: %s", category.category_name)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=category,
            )
        except Exception as exception:
            logger.exception("Error retrieving category with ID %d", id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_category_service(id: int, category_dto: CategoryDTO, session):
        """Update category details."""
        try:
            if not category_dto:
                logger.warning("Attempt to update with empty DTO")
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )

            category_vo = CategoryDAO.get_category_by_id_dao(session, id)
            if not category_vo:
                logger.warning("Category not found for update: ID %d", id)
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )

            category_vo.category_name = category_dto.category_name
            category_vo.category_description = category_dto.category_description
            category_vo.modified_at = get_current_timestamp()
            updated_category = CategoryDAO.update_category_dao(category_vo, session)

            logger.info("Category updated successfully: ID %d", id)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_category,
            )
        except Exception as exception:
            logger.exception("Error updating category with ID %d", id)
            return AppServices.handle_exception(exception)