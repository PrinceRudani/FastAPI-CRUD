from fastapi import APIRouter

from base.api.controller.category import category_controller

router = APIRouter()

router.include_router(category_controller.category_router)
