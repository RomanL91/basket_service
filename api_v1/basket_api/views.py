from fastapi import APIRouter, Response, HTTPException, status

from sqlalchemy.exc import NoResultFound

# == My
from basket_app import schemas
from api_v1.basket_api.depends import UOF_Depends
from basket_app.bascket_service import BascketService


router = APIRouter(tags=["Bascket"])


# CREATE        === === === === === === === ===
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.BasketPydantic | schemas.SimpleMSGErrorPydantic,
    summary="Создание корзины.",
    description="Создай корзину. Смотри пример тела. Из обязательно 'uuid_id'.",
)
async def create_bascket(
    new_bascket: schemas.BasketPydantic, uow: UOF_Depends, response: Response
):
    try:
        return await BascketService().create_bascket(uow=uow, new_bascket=new_bascket)
    except HTTPException as error:
        response.status_code = error.status_code
        response_msg = schemas.SimpleMSGErrorPydantic(
            status_code=error.status_code, message=error.detail
        )
        return response_msg


# GET ALL       === === === === === === === ===
@router.get(
    "/",
    response_model=list[schemas.BasketPydantic],
    summary="Получение списка корзин.",
    description="Можно получить список всех корзин. А нафиг? Пока пусть будет.",
    deprecated=True,
)
async def get_basckets(uow: UOF_Depends):
    return await BascketService().get_baskets(uow)


# GET           === === === === === === === ===
@router.get(
    "/{uuid_id}/",
    response_model=schemas.BasketPydantic | schemas.SimpleMSGErrorPydantic,
    summary="Получение экземпляра корзины по uuid_id.",
    description="""Нужен uuid_id для получения экземпляра корзины. 
                Вернет корзину с completed = False""",
)
async def get_bascket_by_uuid(
    uuid_id: str,
    uow: UOF_Depends,
):
    try:
        return await BascketService().get_bascket_by_uuid(uow=uow, uuid_id=uuid_id)
    except NoResultFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Корзина с UUID {uuid_id!r} не найдена.",
        )


# UPDATE PUT    === === === === === === === ===
# @router.put(
#     "/{uuid_id}/",
#     response_model=schemas.BasketPydantic,
#     summary="Обновит всю корзину.",
#     description="В теле запроса можно указать то поле, которое нужно обновить.",
# )
# async def update_bascket(
#     uow: UOF_Depends,
#     uuid_id: str,
#     bascket_update: schemas.BasketPydantic,
# ):
#     return await BascketService().update_bascket(
#         uow=uow, uuid_id=uuid_id, bascket_update=bascket_update
#     )


# UPDATE PATCH  === === === === === === === ===
@router.patch(
    "/{uuid_id}/",
    response_model=schemas.BasketPydantic,
    summary="Обновит поле корзины.",
    description="В теле запроса можно указать то поле, которое нужно обновить.",
)
async def update_bascket(
    uow: UOF_Depends,
    uuid_id: str,
    bascket_update: schemas.BasketPydantic,
):
    return await BascketService().update_bascket(
        uow=uow, uuid_id=uuid_id, bascket_update=bascket_update, partial=True
    )


# DELETE        === === === === === === === ===
@router.delete(
    "/{uuid_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удали корзину.",
    description="Удалит корзину безвозвратно.",
)
async def delete_bascket(uow: UOF_Depends, uuid_id: str) -> None:
    await BascketService().delete_bascket(uow=uow, uuid_id=uuid_id)


@router.post(
    "/create_or_update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.BasketPydantic,
    summary="Создай или обнови корзину.",
    description="""Создаст новую корзину, если она не существует, 
                или обновит существующию. Из обязательно 'uuid_id'.""",
    responses={500: {"description": "Да пошел ты!"}},
    response_description="Информация о корзине.",
)
async def create_or_update_basket(
    new_bascket: schemas.BasketPydantic,
    uow: UOF_Depends,
    response: Response,
):
    try:
        uuid_id = new_bascket.uuid_id
        return await BascketService().create_or_update_bascket(
            uow=uow, uuid_id=uuid_id, bascket_data=new_bascket
        )
    except NoResultFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Корзина с UUID {uuid_id!r} не найдена.",
        )
