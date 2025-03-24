from base.config.logger_config import get_logger
from base.custom_enum.http_enum import ResponseMessageEnum, HttpStatusCodeEnum
from base.dao.subcategory.subcategory_dao import SubcategoryDAO
from base.dto.subcategory.subcategory_dto import SubcategoryDTO
from base.utils.custom_exception import AppServices
from base.utils.time_stamp import get_current_timestamp
from base.vo.subcategory_vo import SubcategoryVO

logger = get_logger()

class SubcategoryService:
    @staticmethod
    def insert_subcategory_service(subcategory_dto: SubcategoryDTO, session):
        """Convert DTO to Model & Insert Subcategory."""
        try:
            if not subcategory_dto:
                logger.warning("Attempt to insert an empty subcategory DTO")
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )

            subcategory_vo = SubcategoryVO(**subcategory_dto.model_dump())
            subcategory_vo.created_at = get_current_timestamp()
            subcategory_vo.modified_at = get_current_timestamp()
            result = SubcategoryDAO.insert_subcategory_dao(subcategory_vo, session)

            logger.info("Subcategory inserted successfully: %s", subcategory_vo.subcategory_name)
            return AppServices.app_response(
                HttpStatusCodeEnum.CREATED.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=result,
            )
        except Exception as exception:
            logger.exception("Error inserting subcategory")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_all_subcategories_service(session):
        """Fetch all subcategories using SubcategoryDAO."""
        try:
            subcategories = SubcategoryDAO.get_all_subcategories_dao(session)
            logger.info("Fetched %d subcategories", len(subcategories))
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=subcategories,
            )
        except Exception as exception:
            logger.exception("Error fetching subcategories")
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_subcategory_service(id: int, session):
        """Soft delete a subcategory by ID."""
        try:
            result = SubcategoryDAO.delete_subcategory_dao(id, session)
            logger.info("Subcategory deleted: ID %d", id)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=result,
            )
        except Exception as exception:
            logger.exception("Error deleting subcategory with ID %d", id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_subcategory_by_id_service(id: int, session):
        """Retrieve subcategory details for editing."""
        try:
            subcategory = SubcategoryDAO.get_subcategory_by_id_dao(id, session)
            if not subcategory:
                logger.warning("Subcategory not found: ID %d", id)
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )
            logger.info("Subcategory retrieved: %s", subcategory.subcategory_name)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=subcategory,
            )
        except Exception as exception:
            logger.exception("Error retrieving subcategory with ID %d", id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_subcategory_service(id: int, subcategory_dto: SubcategoryDTO, session):
        """Update subcategory details."""
        try:
            if not subcategory_dto:
                logger.warning("Attempt to update with empty DTO")
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )

            subcategory_vo = SubcategoryDAO.get_subcategory_by_id_dao(id, session)
            if not subcategory_vo:
                logger.warning("Subcategory not found for update: ID %d", id)
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                )

            subcategory_vo.subcategory_name = subcategory_dto.subcategory_name
            subcategory_vo.subcategory_description = subcategory_dto.subcategory_description
            subcategory_vo.modified_at = get_current_timestamp()
            updated_subcategory = SubcategoryDAO.update_subcategory_dao(subcategory_vo, session)

            logger.info("Subcategory updated successfully: ID %d", id)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_subcategory,
            )
        except Exception as exception:
            logger.exception("Error updating subcategory with ID %d", id)
            return AppServices.handle_exception(exception)
