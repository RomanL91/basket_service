# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

# == My
from core import settings
from core.base_UOW import IUnitOfWork
from core.base_utils import get_total_sum_per_basket
from order_app.api_bank import ApiPayBank
from order_app.models import Order, TransactionPayment
from basket_app.models import Basket
from order_app.schemas import (
    OrderStatusType,
    OrderCreateSchema,
    PaymentType,
    PaymentStatus,
    BankCallbackModel,
)
from basket_app.schemas import CheckoutStageSchema

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate


class OrdertService:
    async def create_order(self, uow: IUnitOfWork, new_order: OrderCreateSchema):
        comment = new_order.comment or "=)"
        try:
            async with uow:
                basket = await uow.bascket.get_obj(
                    uuid_id=new_order.uuid_id, completed=False
                )
                if basket is None:
                    raise ValueError(
                        "Нет корзины. Возможно, она уже оформлена 'completed=True'"
                    )
                total_sum = get_total_sum_per_basket(
                    shipping_city=new_order.shipping_city,
                    basket_items=basket.basket_items,
                )
                user_id = new_order.access_token.model_dump().get("access_token")
                order_dict = new_order.model_dump(exclude=["access_token"])
                order_dict["user_id"] = user_id.get("user_id", None)
                order_dict["total_amount"] = total_sum

                order: Order = await uow.order.get_obj(
                    max_age_days=settings.api_bank.expire_period,
                    user_id=order_dict["user_id"],
                    total_amount=total_sum,
                    phone_number=new_order.phone_number,
                    email=new_order.email,
                )
                if order:
                    return order.payment_link
                else:
                    order: Order = await uow.order.create_obj(order_dict)
                    basket.checkout_stage = CheckoutStageSchema.IN_PROGRESS
                    if new_order.payment_type == PaymentType.ONLINE:
                        payment_link = await ApiPayBank.create_payment_link(
                            invoice_id=str(order.account_number),
                            amount=int(order.total_amount),
                            description=comment,
                            recipient_contact=order.email,
                            recipient_contact_sms=order.phone_number,
                            notifier_contact_sms=order.phone_number,
                        )
                    else:
                        payment_link = settings.api_bank.self_link_order_dateil
                    order.payment_link = payment_link

                await uow.commit()
                return payment_link

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
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Для корзины {new_order.uuid_id!r} нарушена структура.\n err: {e}",
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

    async def accepting_payment(self, uow: IUnitOfWork, new_payment: BankCallbackModel):
        try:
            new_payment_dict = new_payment.model_dump()
            invoice_id = int(new_payment_dict.get("invoice_id"))
            new_payment_dict["invoice_id"] = invoice_id

            async with uow:
                payment: TransactionPayment = await uow.payment.create_obj_pay(
                    account_id=new_payment.account_id,
                    amount=new_payment.amount,
                    approval_code=new_payment.approval_code,
                    card_id=new_payment.card_id,
                    card_mask=new_payment.card_mask,
                    card_type=new_payment.card_type,
                    code=new_payment.code,
                    currency=new_payment.currency,
                    date_time=new_payment.date_time,
                    description=new_payment.description,
                    email=new_payment.email,
                    ip=new_payment.ip,
                    ip_city=new_payment.ip_city,
                    ip_country=new_payment.ip_country,
                    ip_district=new_payment.ip_district,
                    ip_latitude=new_payment.ip_latitude,
                    ip_longitude=new_payment.ip_longitude,
                    ip_region=new_payment.ip_region,
                    issuer=new_payment.issuer,
                    language=new_payment.language,
                    name=new_payment.name,
                    phone=new_payment.phone,
                    reason=new_payment.reason,
                    reason_code=new_payment.reason_code,
                    reference=new_payment.reference,
                    secure=new_payment.secure,
                    secure_details=new_payment.secure_details,
                    terminal=new_payment.terminal,
                    invoice_id=int(new_payment.invoice_id),
                )
                order: Order = await uow.order.get_obj(
                    account_number=int(new_payment.invoice_id)
                )
                basket: Basket = await uow.bascket.update_ob_pay(
                    uuid_id=order.uuid_id,
                    data={"completed": True, "user_id": order.user_id},
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
