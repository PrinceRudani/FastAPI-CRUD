from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Request,
    Response,
    Depends,
    BackgroundTasks,
    Path,
)

from base.api.controller.notification.notification_controller import (
    NotificationController,
)
from base.config.logger_config import get_logger
from base.custom_enum.static_enum import StaticVariables
from base.middleware.api_key_validator import verify_api_key
from base.service.login.login_service import login_required
from base.service.product.product_service import ProductService
from base.utils.custom_exception import AppServices

logger = get_logger()

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    responses={404: {"description": "API endpoint not found"}},
)


@product_router.post("/insert", dependencies=[Depends(verify_api_key)])
@login_required(required_roles=[StaticVariables.ADMIN_ROLE])
def insert_product_controller(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
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
            background_tasks,
            product_category_id,
            product_subcategory_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_images,
        )

        return response_payload

    except Exception as exception:
        logger.exception("Error inserting product")
        return AppServices.handle_exception(exception)


@product_router.get("/view", dependencies=[Depends(verify_api_key)])
def get_all_products_controller():
    response_payload = ProductService.get_all_products_service()  # the
    return response_payload
    # coroutine


@product_router.get("/view/{id}", dependencies=[Depends(verify_api_key)])
def get_product_by_id_controller(
    response: Response, id: int, background_tasks: BackgroundTasks
):
    response_payload = ProductService.get_product_by_id_service(id, background_tasks)
    return response_payload


@product_router.delete("/delete/{id}", dependencies=[Depends(verify_api_key)])
def delete_product_controller(
    response: Response, id: int, background_tasks: BackgroundTasks
):

    response_payload = ProductService.delete_product_service(id, background_tasks)
    return response_payload


@product_router.put("/update/{id}", dependencies=[Depends(verify_api_key)])
def update_product_controller(
    response: Response,
    background_tasks: BackgroundTasks,
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
            background_tasks,
            id,
            product_category_id,
            product_subcategory_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_images,
        )

        return response_payload

    except Exception as exception:
        logger.exception("Error updating product")
        return AppServices.handle_exception(exception)
