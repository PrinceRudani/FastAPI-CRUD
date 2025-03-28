from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
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
            if not category_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Category inserted successfully: %s", category_vo.category_name)
            return AppServices.app_response(
                HttpStatusCodeEnum.CREATED.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=category_insert_data,
            )
        except Exception as exception:
            logger.exception("Error inserting category")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_all_categories_service():
        """Fetch all categories using CategoryDAO."""
        try:
            get_all_category_data = CategoryDAO.get_all_categories_dao()
            if not get_all_category_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=get_all_category_data,
            )
        except Exception as exception:
            logger.exception("Error fetching all categories")
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_category_service(id):
        """Soft delete a category by ID."""
        try:
            delete_category_data = CategoryDAO.delete_category_dao(id)
            delete_category_data.is_deleted = True
            if not delete_category_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_category_data,
            )

        except Exception as exception:
            logger.exception("Error deleting category")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_category_by_id_service(id):
        """Retrieve category details for editing."""
        try:
            get_category_detail = CategoryDAO.get_category_by_id_dao(id)
            if not get_category_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=get_category_detail,
            )
        except Exception as exception:
            logger.exception("Error retrieving category with ID %d", id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_category_service(category_data):
        """Update category details."""
        try:

            category_vo = CategoryVO()
            category_vo.id = category_data.id
            category_vo.category_name = category_data.category_name
            category_vo.category_description = category_data.category_description

            category_vo.modified_at = get_current_timestamp()
            updated_category_data = CategoryDAO.update_category_dao(category_vo)
            if not updated_category_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_category_data,
            )

        except Exception as exception:
            logger.exception("Error updating category with ID %d", id)
            return AppServices.handle_exception(exception)
