from enum import Enum
from typing import Annotated, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# Определение этапов оформления
class CheckoutStageSchema(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"


class SimpleMSGErrorPydantic(BaseModel):
    status_code: int
    message: str


class BasketPydantic2(BaseModel):
    model_config = ConfigDict(
        strict=True,
    )

    uuid_id: Annotated[
        str,
        Field(
            ...,
            description="Уникальный ID с клиента",
            examples=[
                "fcff9649-c7cc-498c-8ee2-c84785a68521",
            ],
        ),
    ]
    user_id: Annotated[
        Optional[str],
        Field(
            str,
            description="Уникальный ID пользователя",
            alias="token",
            examples=[
                "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOWNhOTAxMzctZGUyOS00NThjLWFjYjgtMDNkZDUzNWFhYjBkIiwidHlwZSI6InJlZnJlc2hfdG9rZW4iLCJleHAiOjE3NDA5MTU5NzMsImlhdCI6MTczODMyMzk3M30.WCz-6i9NYxtlIJ2yLJL6gTrg1v6_3jyd4qRcA1GxKWQSIyCLpkl4FNVpeJuUB4kj9d4rYMET77CvPmwSyXRxTH8IMggQL9-QzpwjkHY3BZs0hIEHSfAzo3QIidNwoLKRA_VcgKEIEro_KVRFgdeaNl2sttoNEWT2UBxOxH-kSmEBSz_4x7q1OsgHB7zxjZgN58iqgl0lDbrlKTViDO-61F9-H8LKOBpvTR1Df6bng1i8lR7C50wSqa3QJus-_Oq67Zts4DQVa1JhuxTmezP4t_Brp5UK3L2f6Z6sQITRuZFPbhEGoiGBqlsB49TWU91s5cZt0iX2C5Qh3gYBhPgBdA",
            ],
        ),
    ] = None
    basket_items: Annotated[
        # TODO улучшить аннотацию
        List[int] | None,
        Field(
            ...,
            description="Состав корзины",
            examples=[
                [
                    1,
                    2,
                    3,
                ]
            ],
        ),
    ] = None


class BasketPydantic(BaseModel):
    model_config = ConfigDict(
        strict=True,
        json_schema_extra={
            "example": {
                "uuid_id": "fcff9649-c7cc-498c-8ee2-c84785a68521",
                "basket_items": [
                    {
                        "prod_id": 1,
                        "count": 5,
                        "price": 799,
                    },
                    {
                        "prod_id": 2,
                        "count": 3,
                        "price": 4599,
                        "gift_prod_id": 1,
                    },
                ],
                # gift_items не включается в пример
            }
        },
    )

    uuid_id: Annotated[
        str,
        Field(
            ...,
            description="Уникальный ID с клиента",
        ),
    ] = None
    user_id: Annotated[
        Optional[str],
        Field(
            str,
            description="Уникальный ID пользователя",
        ),
    ] = None
    completed: Annotated[
        bool | None,
        Field(
            ...,
            description="Статус корзины",
            examples=[False],
        ),
    ] = False
    basket_items: Annotated[
        # TODO улучшить аннотацию
        List[Dict[str, str | int | dict | list]] | None,
        Field(
            ...,
            description="Состав корзины",
        ),
    ] = None
    gift_items: Annotated[
        # TODO улучшить аннотацию
        List[Dict[str, str | int | Dict | List | None]] | None,
        Field(
            ...,
            description="Список подарков",
        ),
    ] = None


class BasketItemUpdate(BaseModel):
    model_config = ConfigDict(
        strict=True,
    )

    count: Annotated[
        int,
        Field(
            ...,
            # description=
        ),
    ]
    delete: Annotated[
        bool,
        Field(
            ...,
            # description=
        ),
    ] = False
