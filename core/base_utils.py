from decimal import Decimal

import jwt

from core import settings


def check_token(jwt_value: str) -> bool:
    try:
        payload_data = jwt.decode(
            jwt_value,
            settings.auth_jwt.public_key,
            settings.auth_jwt.algorithm,
        )
        if payload_data["type"] != settings.auth_jwt.allowed_key_type:
            return False
        return payload_data
    except:
        return False


def get_total_sum_per_basket(shipping_city: str, basket_items: list) -> Decimal:
    total_amount_to_order = []
    try:
        for el in basket_items:
            count = el.get("count", 0)
            price = Decimal(el.get("prod").get("price").get(shipping_city))
            total_amount_to_pos = price * count
            total_amount_to_order.append(total_amount_to_pos)
        total_sum = sum(total_amount_to_order)
        return Decimal(total_sum)
    except (KeyError, TypeError):
        raise ValueError("Нарушение структуры корзины.")
