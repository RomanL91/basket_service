# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

# == My
from core import settings
from core.base_UOW import IUnitOfWork
from core.base_utils import get_total_sum_per_basket
from order_app.api_bank import ApiPayBank
from order_app.models import Order, TransactionPayment
from order_app.schemas import (
    OrderStatusType,
    OrderCreateSchema,
    PaymentType,
    PaymentStatus,
    TransactionPaymentSchema,
)
from basket_app.schemas import CheckoutStageSchema

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate


class OrdertService:
    async def create_order(self, uow: IUnitOfWork, new_order: OrderCreateSchema):
        comment = new_order.comment or ""
        try:
            async with uow:
                basket = await uow.bascket.get_obj(
                    uuid_id=new_order.uuid_id, completed=False
                )
                total_sum = get_total_sum_per_basket(
                    shipping_city=new_order.shipping_city,
                    basket_items=basket.basket_items,
                )
                user_id = new_order.access_token.model_dump().get("access_token")
                order_dict = new_order.model_dump(exclude=["access_token"])
                order_dict["user_id"] = user_id.get("user_id", None)
                order_dict["total_amount"] = total_sum
                order: Order = await uow.order.create_obj(order_dict)
                basket.checkout_stage = CheckoutStageSchema.IN_PROGRESS
                await uow.commit()
                if new_order.payment_type == PaymentType.ONLINE:
                    return await ApiPayBank.create_payment_link(
                        invoice_id=str(order.account_number),
                        amount=int(order.total_amount),
                        description=comment,
                        recipient_contact=order.email,
                        recipient_contact_sms=order.phone_number,
                        notifier_contact_sms=order.phone_number,
                    )
                else:
                    return settings.api_bank.self_link_order_dateil

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Упсс ... ограничения базы данных.",
            )
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Не нашел корзину с {new_order.uuid_id!r} для создания заказа.",
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Для корзины {new_order.uuid_id!r} нарушена структура.",
            )

    async def get_orders_by_user_id(self, uow: IUnitOfWork, user_id: str):
        async with uow:
            orders = await uow.order.get_objs_to_user_id(user_id=user_id)
            return orders

    async def get_info_order_with_basket(self, uow: IUnitOfWork, uuid_id: str):
        async with uow:
            res = await uow.order.get_info_order_with_basket(uuid_id=uuid_id)
            return res

    async def get_paginated_orders(
        self, uow: IUnitOfWork, params: Params, order_status: OrderStatusType
    ) -> Page:
        async with uow:
            query = uow.order.get_query_orders(
                order_status
            )  # Получаем базовый запрос на объекты Order
            result = await paginate(uow.session, query, params)
            return result

    async def get_paginated_orders_by_filters(
        self, uow: IUnitOfWork, params: Params, **kwargs
    ) -> Page:
        async with uow:
            query = uow.order.get_objs_by_filters(**kwargs)
            result = await paginate(uow.session, query, params)
            return result

    async def accepting_payment(
        self, uow: IUnitOfWork, new_payment: TransactionPaymentSchema
    ):
        try:
            new_payment_dict = new_payment.model_dump()
            async with uow:
                payment: TransactionPayment = await uow.payment.create_obj(
                    new_payment_dict
                )
                order: Order = await uow.order.get_obj(
                    account_number=new_payment.invoice_id
                )
                if order.total_amount != payment.amount:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Платеж не соотвествует сумме ордера.",
                    )
                order.payment_status = PaymentStatus.PAID
                await uow.commit()
            return None
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Упсс ... ограничения базы данных.",
            )
