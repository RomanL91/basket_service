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
