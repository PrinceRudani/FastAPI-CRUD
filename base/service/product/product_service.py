from fastapi import UploadFile

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.category.category_dao import CategoryDAO
from base.dao.product.product_dao import ProductDAO
from base.dao.subcategory.subcategory_dao import SubcategoryDAO
from base.utils.custom_exception import AppServices
from base.utils.image_store import ProductImageUploader
from base.utils.time_stamp import get_current_timestamp
from base.vo.product_vo import ProductVO

logger = get_logger()
UPLOAD_DIR = "static/product_image/"


class ProductService:
    @staticmethod
    def insert_product_service(
            product_category_id,
            product_subcategory_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_images,
    ):
        try:
            # Validate Category and Subcategory
            category = CategoryDAO.get_category_by_id_dao(product_category_id)
            subcategory = SubcategoryDAO.get_subcategory_by_id_dao(
                product_subcategory_id)

            if not category or category.is_deleted:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST,
                    ResponseMessageEnum.NOT_FOUND,
                    success=False,
                    data={},
                )
            if not subcategory or subcategory.is_deleted:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST,
                    ResponseMessageEnum.NOT_FOUND,
                    success=False,
                    data={},
                )

            # Save images safely
            image_name, image_path = ProductImageUploader.save_image(
                product_images)

            product_data = {
                "product_category_id": product_category_id,
                "product_subcategory_id": product_subcategory_id,
                "product_name": product_name,
                "product_description": product_description,
                "product_price": product_price,
                "product_quantity": product_quantity,
                "product_image_names": image_name,
                "product_image_paths": image_path,
                "is_deleted": False,
                "created_at": get_current_timestamp(),
                "modified_at": get_current_timestamp(),
            }

            # Insert product
            product_vo = ProductVO(**product_data)
            product_insert_data = ProductDAO.insert_product_dao(product_vo)

            return AppServices.app_response(
                HttpStatusCodeEnum.CREATED.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=product_insert_data,
            )

        except Exception as exception:
            logger.exception("Error inserting product")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_all_products_service():
        """Retrieve all products."""
        try:
            products = ProductDAO.get_all_product_dao()
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=products,
            )
        except Exception as exception:
            logger.exception("Error fetching products")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_product_by_id_service(id):
        """Retrieve product by id."""
        try:
            product = ProductDAO.get_product_by_id_dao(id)
            product
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=product,
            )
        except Exception as exception:
            logger.exception("Error fetching product")
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_product_service(id):
        """Soft delete a product by ID."""
        try:
            deleted_product = ProductDAO.delete_product_dao(id)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=deleted_product,
            )
        except Exception as exception:
            logger.exception("Error deleting product")
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_product_service(
            id,
            product_category_id,
            product_subcategory_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_images: UploadFile,
    ):
        """Update product, replacing image only if a new one is uploaded."""
        try:
            existing_product = ProductDAO.get_product_by_id_dao(id)
            if not existing_product:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            # Validate Category
            category = CategoryDAO.get_category_by_id_dao(product_category_id)
            if not category or getattr(category, "is_deleted", False):
                logger.info(
                    "Attempt to update product with deleted or non-existent category ID: %d",
                    product_category_id,
                )
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    "Cannot update product under a deleted category.",
                    success=False,
                )

            # Validate Subcategory (Fixing NoneType issue)
            subcategory = SubcategoryDAO.get_subcategory_by_id_dao(
                product_subcategory_id)
            if subcategory is None or getattr(subcategory, "is_deleted",
                                              False):
                logger.info(
                    "Attempt to update product with deleted or non-existent subcategory ID: %d",
                    product_subcategory_id,
                )
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    "Cannot update product under a deleted subcategory.",
                    success=False,
                )

            # Preserve existing image unless a new one is uploaded
            image_name = existing_product.product_image_names
            image_path = existing_product.product_image_paths

            if product_images:
                image_name, image_path = (
                    ProductImageUploader.save_image(product_images))
                print(">>>>>>>>>>>", image_path)
                print(">>>>>>>>>>>", image_name)
            # Prepare updated product data
            product_data = {
                "id": id,
                "product_name": product_name,
                "product_description": product_description,
                "product_price": product_price,
                "product_category_id": product_category_id,
                "product_subcategory_id": product_subcategory_id,
                "product_image_names": image_name,
                "product_image_paths": image_path,
                "product_quantity": product_quantity,
                "modified_at": get_current_timestamp(),
            }

            # Update the product
            product_vo = ProductVO(**product_data)
            updated_product_data = ProductDAO.update_product_dao(product_vo)

            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_product_data,
            )

        except Exception as exception:
            logger.exception(f"Error updating product: {exception}")
            return AppServices.handle_exception(exception)
