# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# == My
from core.base_UOW import IUnitOfWork
from order_app.models import Order
from order_app.schemas import OrderPydantic, OrderStatusType

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate


class OrdertService:
    async def create_order(
        self, uow: IUnitOfWork, new_order: OrderPydantic
    ) -> Order | None:
        order_dict = new_order.model_dump()
        async with uow:
            try:
                order = await uow.order.create_obj(order_dict)
                await uow.commit()
                return order
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ордер {new_order.uuid_id!r} уже существует.",
                )

    async def get_orders(self, uow: IUnitOfWork) -> list[Order]:
        async with uow:
            return await uow.order.get_all_objs()

    async def get_order_by_uuid(self, uow: IUnitOfWork, uuid_id: str) -> Order:
        async with uow:
            return await uow.order.get_obj(uuid_id=uuid_id)

    async def update_order(
        self,
        uow: IUnitOfWork,
        uuid_id: str,
        order_update: OrderPydantic,
        partial: bool = False,
    ) -> Order:
        data = order_update.model_dump(exclude_unset=partial)
        async with uow:
            order = await uow.order.update_obj(uuid_id=uuid_id, data=data)
            await uow.commit()
            return order

    async def delete_order(self, uow: IUnitOfWork, uuid_id: str) -> None:
        async with uow:
            await uow.order.delete_obj(uuid_id=uuid_id)
            await uow.commit()

    async def get_info_order_with_basket(self, uow: IUnitOfWork, uuid_id: str):
        async with uow:
            res = await uow.order.get_info_order_with_basket(uuid_id=uuid_id)
            await uow.commit()
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
