from fastapi import APIRouter, status

from order_app.order_service import OrdertService
from api_v1.order_api.depends import UOF_Depends
from order_app.schemas import (
    TransactionPaymentSchema,
)


router = APIRouter(tags=["Payment"])


@router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="endpoint для обратного вызова от банка",
    description="""
    После совершения оплаты с формы оплаты от банка, последний 
    совершает обратный вызов на данный endpoint.
    Создается запись о результате платежа и закреплятся за ордером,
    переводя статус последнего в состояние - оплачен.
    """,
)
async def test_payment(
    new_payment: TransactionPaymentSchema,
    uow: UOF_Depends,
):
    await OrdertService().accepting_payment(uow=uow, new_payment=new_payment)
