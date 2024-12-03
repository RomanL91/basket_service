from fastapi import APIRouter

from .basket_api.views import router as bascket_router
from .order_api.views import router as order_router
from .payment_api.view import router as payment_router


router = APIRouter()

router.include_router(router=bascket_router, prefix="/bascket")
router.include_router(router=order_router, prefix="/order")
router.include_router(router=payment_router, prefix="/payment")
