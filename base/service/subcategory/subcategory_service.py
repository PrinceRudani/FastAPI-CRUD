from base.config.logger_config import get_logger
from base.custom_enum.http_enum import ResponseMessageEnum, HttpStatusCodeEnum
from base.dao.category.category_dao import CategoryDAO
from base.dao.subcategory.subcategory_dao import SubcategoryDAO
from base.utils.custom_exception import AppServices
from base.utils.time_stamp import get_current_timestamp
from base.vo.subcategory_vo import SubcategoryVO

logger = get_logger()


class SubcategoryService:
    @staticmethod
    def insert_subcategory_service(subcategory_dto):
        """Convert DTO to Model & Insert Subcategory."""
        try:
            if not subcategory_dto:
                logger.warning("Attempt to insert an empty subcategory DTO")
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )
            category = CategoryDAO.get_category_by_id_dao(
                subcategory_dto.subcategory_category_id)
            if not category:
                logger.warning(
                    "Attempt to insert subcategory with deleted category ID: %d",
                    subcategory_dto.subcategory_category_id)
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    "Cannot insert subcategory under a deleted category.",
                    success=False,
                )

            subcategory_vo = SubcategoryVO()
            subcategory_vo.subcategory_category_id = subcategory_dto.subcategory_category_id
            subcategory_vo.subcategory_name = subcategory_dto.subcategory_name
            subcategory_vo.subcategory_description = subcategory_dto.subcategory_description
            subcategory_vo.created_at = get_current_timestamp()
            subcategory_vo.modified_at = get_current_timestamp()
            subcategory_insert_data = SubcategoryDAO.insert_subcategory_dao(
                subcategory_vo)

            logger.info("Subcategory inserted successfully: %s",
                        subcategory_vo.subcategory_name)
            return AppServices.app_response(
                HttpStatusCodeEnum.CREATED.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=subcategory_insert_data,
            )
        except Exception as exception:
            logger.exception("Error inserting subcategory")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_all_subcategories_service():
        """Fetch all subcategories using SubcategoryDAO."""
        try:
            get_all_subcategory_data = (
                SubcategoryDAO.get_all_subcategories_dao())
            logger.info("Fetched %d subcategories",
                        len(get_all_subcategory_data))
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=get_all_subcategory_data,
            )
        except Exception as exception:
            logger.exception("Error fetching subcategories")
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_subcategory_service(id):
        """Soft delete a subcategory by ID."""
        try:
            delete_subcategory_data = SubcategoryDAO.delete_subcategory_dao(id)
            logger.info("Subcategory deleted: ID %d", id)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_subcategory_data,
            )
        except Exception as exception:
            logger.exception("Error deleting subcategory with ID %d", id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_subcategory_by_id_service(id: int):
        """Retrieve subcategory details for editing."""
        try:
            get_subcategory_detail = (
                SubcategoryDAO.get_subcategory_by_id_dao(id))
            if not get_subcategory_detail:
                logger.warning("Subcategory not found: ID %d", id)
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )
            logger.info("Subcategory retrieved: %s",
                        get_subcategory_detail.subcategory_name)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=get_subcategory_detail,
            )
        except Exception as exception:
            logger.exception("Error retrieving subcategory with ID %d", id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_subcategory_service(update_subcategory_dto):
        """Update subcategory details."""
        try:
            subcategory_vo = SubcategoryVO()
            subcategory_vo.id = update_subcategory_dto.id
            subcategory_vo.subcategory_category_id = update_subcategory_dto.subcategory_category_id
            subcategory_vo.subcategory_name = update_subcategory_dto.subcategory_name
            subcategory_vo.subcategory_description = update_subcategory_dto.subcategory_description
            subcategory_vo.modified_at = get_current_timestamp()
            updated_subcategory_data = SubcategoryDAO.update_subcategory_dao(
                subcategory_vo
            )

            logger.info("Subcategory updated successfully")
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_subcategory_data,
            )
        except Exception as exception:
            return AppServices.handle_exception(exception)
