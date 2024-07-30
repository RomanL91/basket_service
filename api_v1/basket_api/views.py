from fastapi import APIRouter, Response, HTTPException, status

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
)
async def get_basckets(uow: UOF_Depends):
    return await BascketService().get_baskets(uow)


# GET           === === === === === === === ===
@router.get(
    "/{uuid_id}/",
    response_model=schemas.BasketPydantic,
)
async def get_bascket_by_uuid(uuid_id: str, uow: UOF_Depends):
    return await BascketService().get_bascket_by_uuid(uow=uow, uuid_id=uuid_id)


# UPDATE PUT    === === === === === === === ===
@router.put(
    "/{uuid_id}/",
    response_model=schemas.BasketPydantic,
)
async def update_bascket(
    uow: UOF_Depends,
    uuid_id: str,
    bascket_update: schemas.BasketPydantic,
):
    return await BascketService().update_bascket(
        uow=uow, uuid_id=uuid_id, bascket_update=bascket_update
    )


# UPDATE PATCH  === === === === === === === ===
@router.patch(
    "/{uuid_id}/",
    response_model=schemas.BasketPydantic,
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
)
async def delete_bascket(uow: UOF_Depends, uuid_id: str) -> None:
    await BascketService().delete_bascket(uow=uow, uuid_id=uuid_id)
