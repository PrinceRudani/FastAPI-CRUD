from fastapi import APIRouter

from base.api.controller.category import category_controller
from base.api.controller.subcategory import subcategory_controller

router = APIRouter()

router.include_router(category_controller.category_router)
router.include_router(subcategory_controller.subcategory_router)
