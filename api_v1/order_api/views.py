from fastapi_pagination import Page
from fastapi import APIRouter, HTTPException, status

from sqlalchemy.exc import NoResultFound

# == My
from order_app.order_service import OrdertService
from api_v1.order_api.depends import UOF_Depends, Params_Depends, Token_Depends
from order_app.schemas import (
    OrderCreateSchema,
    OrderPydantic,
    OrderStatusType,
    ReadOrderPydantic,
    TokenSchema,
)


router = APIRouter(tags=["Order"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    # response_model=
    summary="Создание ордера.",
    description="""
    Точка для создания ордера. 
    Результатом данной точки является url ссылка, которая может вести как в ЛК пользователя,
    так и на страницу оплаты, в зависимости от выбранного пользователем способом оплаты.
    Так же есть возможность отдавать ссылку на страницу с ошибкой в случае, если от банка
    не получена платежная ссылка, но код статус 2хх.
    Для взаимодействия требуется ключ доступа типа access и годный по сроку давности.
    Обязательные поля для точки помечены в схеме.
    """,
)
async def create_order(
    new_order: OrderCreateSchema,
    uow: UOF_Depends,
):
    link = await OrdertService().create_order(uow=uow, new_order=new_order)
    return link


# GET ALL WITH PAGINATED    === === === === ===
@router.get(
    "/all/",
    response_model=Page[OrderPydantic],
    summary="Получение всех ордеров с пагинацией.",
    description="""
    Данный endpoint возвращает список ордеров с пагинацией. 
    Можно не переживать о расходе памяти, так как мы не выгружаем из БД
    все ордера в память устройства. Вместо этого оно выполняет SQL-запрос, 
    который включает в себя LIMIT и OFFSET, чтобы получить только нужные 
    записи для конкретной страницы. 
    """,
)
async def get_orders(
    uow: UOF_Depends,
    params: Params_Depends,
    order_status: OrderStatusType = OrderStatusType.NEW,
):
    return await OrdertService().get_paginated_orders(uow, params, order_status)


# GET           === === === === === === === ===
@router.get(
    "/info_with_basket/{uuid_id}/",
    # response_model=
    summary="Получение экземпляра ордера по uuid_id с детальной информацией о корзине.",
    # description=
)
async def get_info_order_with_basket(
    uuid_id: str,
    uow: UOF_Depends,
):
    try:
        return await OrdertService().get_info_order_with_basket(
            uow=uow, uuid_id=uuid_id
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ордер с UUID {uuid_id!r} не найден.",
        )


# GET           === === === === === === === ===
@router.get(
    "/by_access_t/",
    # response_model=,
    summary="Получение экземпляров ордеров через haeders access_token.",
    description="""
        Нужен валидный ключ.
        Вернет список ордеров пользователя.
        """,
)
async def get_order_by_access_token(uow: UOF_Depends, access_token: Token_Depends):
    try:
        data_token = TokenSchema(access_token=access_token)
        user_id = data_token.access_token.get("user_id")
        orders = await OrdertService().get_orders_by_user_id(uow=uow, user_id=user_id)
        return orders
    except ValueError:
        raise HTTPException(400)


# GET ALL WITH PAGINATED AND FILTERING executive_id ===
@router.get(
    "/get_manager_order_archive/{manager_executive_id}/",
    response_model=Page[ReadOrderPydantic],
    summary="Получение ордеров, которые менеджер уже принял в обработку (!=NEW).",
    description="""Нужен manager_executive_id для получения ордеров, 
                с которыми менеджер работал ранее. Принимал или отклонял - 
                все ордера с которыми он взаимодействовал.""",
)
async def get_manager_order_archive(
    manager_executive_id: str,
    params: Params_Depends,
    uow: UOF_Depends,
):
    return await OrdertService().get_paginated_orders_by_filters(
        uow=uow, params=params, manager_executive_id=manager_executive_id
    )
