from fastapi import APIRouter, UploadFile, File, Path, Form, Request, Response

from base.api.controller.notification.notification_controller import \
    NotificationController
from base.config.logger_config import get_logger
from base.custom_enum.static_enum import StaticVariables
from base.service.login.login_service import login_required
from base.service.product.product_service import ProductService
from base.utils.custom_exception import AppServices

logger = get_logger()

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    responses={404: {"description": "API endpoint not found"}},
)


@product_router.post("/insert")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def insert_product_controller(
        request: Request, response: Response,
        product_category_id: int = Form(...),
        product_subcategory_id: int = Form(...),
        product_name: str = Form(...),
        product_description: str = Form(...),
        product_price: int = Form(...),
        product_quantity: int = Form(...),
        product_images: list[UploadFile] = File(...),
):
    try:
        response_payload = ProductService.insert_product_service(
            product_category_id,
            product_subcategory_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_images,
        )
        email_sent = NotificationController.send_email_notification(
            to_email="pinsurudani2003@gmail.com",
            subject="New Product Inserted",
            message=f"Product '{product_name}' was successfully added."
        )
        return response_payload, email_sent

    except Exception as exception:
        logger.exception("Error inserting product")
        return AppServices.handle_exception(exception)


@product_router.get("/view")
def get_all_products_controller():
    response_payload = ProductService.get_all_products_service()  # the
    return response_payload
    # coroutine


@product_router.get("/view/{id}")
def get_product_by_id_controller(response: Response, id: int):
    email_sent = NotificationController.send_email_notification(
        to_email="pinsurudani2003@gmail.com",
        subject=" Product fetched successfully",
        message=f"Product '{id}' was successfully fetched."
    )
    response_payload = ProductService.get_product_by_id_service(id)
    return response_payload, email_sent


@product_router.delete("/delete/{id}")
def delete_product_controller(response: Response, id: int):
    email_sent = NotificationController.send_email_notification(
        to_email="pinsurudani2003@gmail.com",
        subject=" Product deleted successfully",
        message=f"Product '{id}' was successfully deleted."
    )
    response_payload = ProductService.delete_product_service(id)
    return response_payload, email_sent


@product_router.put("/update/{id}")
def update_product_controller(response: Response,
                              id: int = Path(..., title="Product ID"),
                              product_category_id: int = Form(...),
                              product_subcategory_id: int = Form(...),
                              product_name: str = Form(...),
                              product_description: str = Form(...),
                              product_price: int = Form(...),
                              product_quantity: int = Form(...),
                              product_images: UploadFile = File(None),
                              ):
    try:
        response_payload = ProductService.update_product_service(
            id,
            product_category_id,
            product_subcategory_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_images,
        )
        email_sent = NotificationController.send_email_notification(
            to_email="pinsurudani2003@gmail.com",
            subject=" Product updated successfully",
            message=f"Product '{id}' was successfully updated."
        )
        return response_payload, email_sent

    except Exception as exception:
        logger.exception("Error updating product")
        return AppServices.handle_exception(exception)
