from fastapi_pagination import Page
from fastapi import APIRouter, HTTPException, status

from sqlalchemy.exc import NoResultFound

# == My
from order_app.schemas import HttpUrl, OrderCreateSchema
from order_app import schemas
from api_v1.order_api.depends import UOF_Depends, Params_Depends
from order_app.order_service import OrdertService


# TODO этот импорт не совсем уместен, нужен базовый класс пидантик исключений
# а не таскать эту схему во все приложения
# from basket_app.schemas import SimpleMSGErrorPydantic


router = APIRouter(tags=["Order"])


# CREATE        === === === === === === === ===
# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=schemas.OrderPydantic | SimpleMSGErrorPydantic,
#     summary="Создание ордера.",
#     description="Создай ордер. Смотри пример тела.",
# )
# async def create_order(
#     new_order: schemas.CreateOrderPydantic, uow: UOF_Depends, response: Response
# ):
#     try:
#         return await OrdertService().create_order(uow=uow, new_order=new_order)
#     except HTTPException as error:
#         response.status_code = error.status_code
#         response_msg = SimpleMSGErrorPydantic(
#             status_code=error.status_code, message=error.detail
#         )
#         return response_msg


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    # response_model=HttpUrl,  # нужна отдельная модель для ответа
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


# GET ALL       === === === === === === === ===
# @router.get(
#     "/",
#     response_model=list[schemas.ReadOrderPydantic],
#     summary="Получение всех ордеров.",
#     description="Скорее всего это не пригодиться, но пусть пока будет.",
#     deprecated=True,
# )
# async def get_orders(uow: UOF_Depends):
#     return await OrdertService().get_orders(uow)


# GET ALL WITH PAGINATED    === === === === ===
@router.get(
    "/all/",
    response_model=Page[schemas.OrderPydantic],
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
    order_status: schemas.OrderStatusType = schemas.OrderStatusType.NEW,
):
    return await OrdertService().get_paginated_orders(uow, params, order_status)


# GET           === === === === === === === ===
# @router.get(
#     "/{uuid_id}/",
#     response_model=schemas.OrderPydantic | SimpleMSGErrorPydantic,
#     summary="Получение экземпляра ордера по uuid_id.",
#     description="""Нужен uuid_id для получения экземпляра ордера. 
#                 Вернет ордер с completed = False""",
# )
# async def get_order_by_uuid(
#     uuid_id: str,
#     uow: UOF_Depends,
# ):
#     try:
#         return await OrdertService().get_order_by_uuid(uow=uow, uuid_id=uuid_id)
#     except NoResultFound as error:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Ордер с UUID {uuid_id!r} не найден.",
#         )


# UPDATE PATCH  === === === === === === === ===
# @router.patch(
#     "/{uuid_id}/",
#     response_model=schemas.OrderPydantic,
#     summary="Обновит поле ордера.",
#     description="В теле запроса можно указать то поле, которое нужно обновить.",
# )
# async def update_order(
#     uow: UOF_Depends,
#     uuid_id: str,
#     order_update: schemas.OrderPydantic,
# ):
#     return await OrdertService().update_order(
#         uow=uow, uuid_id=uuid_id, order_update=order_update, partial=True
#     )


# DELETE        === === === === === === === ===
# @router.delete(
#     "/{uuid_id}/",
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary="Удали ордер.",
#     description="Удалит ордер безвозвратно.",
# )
# async def delete_order(uow: UOF_Depends, uuid_id: str) -> None:
#     await OrdertService().delete_order(uow=uow, uuid_id=uuid_id)


# GET           === === === === === === === ===
@router.get(
    "/info_with_basket/{uuid_id}/",
    # response_model=schemas.OrderResponse, # TODO сюда нужна пидантик модель
    summary="Получение экземпляра ордера по uuid_id с детальной информацией о корзине.",
    # description="""Нужен uuid_id для получения экземпляра ордера.
    #             Вернет ордер с completed = False""",
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


# GET ALL WITH PAGINATED AND FILTERING executive_id ===
@router.get(
    "/get_manager_order_archive/{manager_executive_id}/",
    response_model=Page[schemas.ReadOrderPydantic],
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
