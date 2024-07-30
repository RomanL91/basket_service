from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class SettingsDataBase(BaseModel):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    echo: bool = True  # Для дебага


class SettingsAuth(BaseModel):
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"


class Settings(BaseSettings):
    api_v1_prefix: str = "/basket_api/v1"
    time_zone: ZoneInfo = ZoneInfo("Asia/Almaty")

    # == DataBase
    db: SettingsDataBase = SettingsDataBase()
    # == Auth
    auth_jwt: SettingsAuth = SettingsAuth()


settings = Settings()
