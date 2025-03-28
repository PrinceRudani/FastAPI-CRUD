from fastapi import APIRouter

from base.api.controller.category import category_controller
from base.api.controller.product import product_controller
from base.api.controller.register import register_controller
from base.api.controller.subcategory import subcategory_controller

router = APIRouter()

# router.include_router(register_controller.register_router)
router.include_router(category_controller.category_router)
router.include_router(subcategory_controller.subcategory_router)
router.include_router(product_controller.product_router)
