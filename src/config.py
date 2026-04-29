from pydantic_settings import BaseSettings, SettingsConfigDict
from aiohttp import ClientSession

class SessionManager:
    _session: ClientSession | None = None

    @classmethod
    async def get_session(cls) -> ClientSession:
        """Возвращает сессию aiohttp, создавая её при первом вызове."""
        if cls._session is None or cls._session.closed:
            cls._session = ClientSession()
        return cls._session

    @classmethod
    async def close_session(cls):
        """Закрывает сессию, если она существует."""
        if cls._session is not None:
            await cls._session.close()
            cls._session = None

class CaptchaSettings(BaseSettings):
    api_key: str
    callback_url: str

    model_config = SettingsConfigDict(env_prefix="RECAPTCHA_", env_file=".env", extra="ignore")

class BitrixSettings(BaseSettings):
    url: str
    webhook_url: str

    model_config = SettingsConfigDict(env_prefix="BITRIX_", env_file=".env", extra="ignore")


class Settings(BaseSettings):
    host: str
    port: int

    captcha: CaptchaSettings
    bitrix: BitrixSettings

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

tasks = {}
settings = Settings(
    captcha=CaptchaSettings(),
    bitrix=BitrixSettings(),
)
