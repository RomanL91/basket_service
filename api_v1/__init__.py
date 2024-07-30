from fastapi import APIRouter

from .basket_api.views import router as bascket_router


router = APIRouter()

router.include_router(router=bascket_router, prefix="/bascket")
