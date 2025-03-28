from fastapi import APIRouter, UploadFile, File, Path, Form

from base.config.logger_config import get_logger
from base.service.product.product_service import ProductService
from base.utils.custom_exception import AppServices

logger = get_logger()

product_router = APIRouter(
    prefix="/product",
    tags=["Product"],
    responses={404: {"description": "API endpoint not found"}},
)


@product_router.post("/insert")
async def insert_product_controller(
    product_category_id: int = Form(...),
    product_subcategory_id: int = Form(...),
    product_name: str = Form(...),
    product_description: str = Form(...),
    product_price: int = Form(...),
    product_quantity: int = Form(...),
    product_images: list[UploadFile] = File(None),
):
    try:
        result = await ProductService.insert_product_service(
            product_category_id,
            product_subcategory_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_images,
        )
        return result

    except Exception as exception:
        logger.exception("Error inserting product")
        return AppServices.handle_exception(exception)


@product_router.get("/view")
async def get_all_products_controller():
    return await ProductService.get_all_products_service()  # Await the coroutine


@product_router.get("/view/{id}")
async def get_product_by_id_controller(id: int):
    return ProductService.get_product_by_id_service(id)


@product_router.delete("/delete/{id}")
async def delete_product_controller(id: int):
    return ProductService.delete_product_service(id)


@product_router.put("/update/{id}")
async def update_product_controller(
    id: int = Path(..., title="Product ID"),
    product_category_id: int = Form(...),
    product_subcategory_id: int = Form(...),
    product_name: str = Form(...),
    product_description: str = Form(...),
    product_price: int = Form(...),
    product_quantity: int = Form(...),
    product_image: UploadFile = File(None),
):
    try:
        result = await ProductService.update_product_service(
            id,
            product_category_id,
            product_subcategory_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_image,
        )
        return result

    except Exception as exception:
        logger.exception("Error updating product")
        return AppServices.handle_exception(exception)
