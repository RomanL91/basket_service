from fastapi import APIRouter, Response, HTTPException, status

from sqlalchemy.exc import NoResultFound

# == My
from order_app import schemas
from api_v1.order_api.depends import UOF_Depends
from order_app.order_service import OrdertService

# TODO этот импорт не совсем уместен, нужен базовый класс пидантик исключений
# а не таскать эту схему во все приложения
from basket_app.schemas import SimpleMSGErrorPydantic


router = APIRouter(tags=["Order"])


# CREATE        === === === === === === === ===
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.OrderPydantic | SimpleMSGErrorPydantic,
    summary="Создание ордера.",
    description="Создай ордер. Смотри пример тела.",
)
async def create_order(
    new_order: schemas.OrderPydantic, uow: UOF_Depends, response: Response
):
    try:
        return await OrdertService().create_order(uow=uow, new_order=new_order)
    except HTTPException as error:
        response.status_code = error.status_code
        response_msg = SimpleMSGErrorPydantic(
            status_code=error.status_code, message=error.detail
        )
        return response_msg


# GET ALL       === === === === === === === ===
@router.get(
    "/",
    response_model=list[schemas.OrderPydantic],
    summary="Получение всех ордеров.",
    description="Скорее всего это не пригодиться, но пусть пока будет.",
    # deprecated=True,
)
async def get_orders(uow: UOF_Depends):
    return await OrdertService().get_orders(uow)


# GET           === === === === === === === ===
@router.get(
    "/{uuid_id}/",
    response_model=schemas.OrderPydantic | SimpleMSGErrorPydantic,
    summary="Получение экземпляра ордера по uuid_id.",
    description="""Нужен uuid_id для получения экземпляра ордера. 
                Вернет ордер с completed = False""",
)
async def get_order_by_uuid(
    uuid_id: str,
    uow: UOF_Depends,
):
    try:
        return await OrdertService().get_order_by_uuid(uow=uow, uuid_id=uuid_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ордер с UUID {uuid_id!r} не найден.",
        )


# UPDATE PATCH  === === === === === === === ===
@router.patch(
    "/{uuid_id}/",
    response_model=schemas.OrderPydantic,
    summary="Обновит поле ордера.",
    description="В теле запроса можно указать то поле, которое нужно обновить.",
)
async def update_order(
    uow: UOF_Depends,
    uuid_id: str,
    order_update: schemas.OrderPydantic,
):
    return await OrdertService().update_order(
        uow=uow, uuid_id=uuid_id, order_update=order_update, partial=True
    )


# DELETE        === === === === === === === ===
@router.delete(
    "/{uuid_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удали ордер.",
    description="Удалит ордер безвозвратно.",
)
async def delete_order(uow: UOF_Depends, uuid_id: str) -> None:
    await OrdertService().delete_order(uow=uow, uuid_id=uuid_id)


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
