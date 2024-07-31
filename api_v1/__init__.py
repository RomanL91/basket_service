from fastapi import APIRouter

from .basket_api.views import router as bascket_router
from .order_api.views import router as order_router


router = APIRouter()

router.include_router(router=bascket_router, prefix="/bascket")
router.include_router(router=order_router, prefix="/order")
