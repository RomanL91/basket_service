from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from fastapi.middleware.cors import CORSMiddleware


BASE_DIR = Path(__file__).parent.parent


class SettingsDataBase(BaseModel):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    echo: bool = True  # Для дебага


class SettingsAuth(BaseModel):
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"


class SettingsCORSMiddleware(BaseModel):
    origins: list[str] = ["http://localhost", "http://localhost:3000"]
    middleware: dict = {
        "middleware_class": CORSMiddleware,
        "allow_origins": origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }


class Settings(BaseSettings):
    # == start app
    app: str = "main:app"
    host: str = "127.0.0.1"
    port: int = 5001
    reload_flag: bool = True

    # == other
    api_v1_prefix: str = "/basket_api/v1"
    time_zone: ZoneInfo = ZoneInfo("Asia/Almaty")

    # == DataBase
    db: SettingsDataBase = SettingsDataBase()
    # == Auth
    auth_jwt: SettingsAuth = SettingsAuth()
    # == CORSMiddleware
    middleware: SettingsCORSMiddleware = SettingsCORSMiddleware()


settings = Settings()
