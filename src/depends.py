from aiohttp import ClientSession

from services.captcha import CaptchaService
from services.sfr import SFRService

from fastapi import Depends
from config import SessionManager


def get_captcha_service(
    http_session: ClientSession = Depends(SessionManager.get_session)
) -> CaptchaService:
    return CaptchaService(
        http_session,
    )

def get_sfr_service(
    http_session: ClientSession = Depends(SessionManager.get_session)
) -> SFRService:
    return SFRService(
        http_session,
    )