from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse
from urllib.parse import parse_qs
from config import tasks
from depends import get_sfr_service, get_captcha_service, get_bitrix_contact_service
from services.bitrix import BitrixContactsService
from services.sfr import SFRService
from aiohttp.client_exceptions import ContentTypeError
from services.captcha import CaptchaService

router = APIRouter(tags=["rucaptcha"])

@router.get("/rucaptcha.txt")
async def install_webhook():
    """Метод для установки webhook для callback когда разгадана капча"""
    return FileResponse(
        "rucaptcha.txt",
    )

@router.get("/task/{task_id}")
async def get_task(
    task_id: str,
    captcha_service: CaptchaService = Depends(get_captcha_service),
):
    """Метод для получения информации о captcha"""
    return await captcha_service.get_task(task_id)

@router.post("/callback")
async def callback(
    request: Request,
    sfr_service: SFRService = Depends(get_sfr_service),
    bitrix_service: BitrixContactsService = Depends(get_bitrix_contact_service)
):
    try:
        body = await request.body()
        data = parse_qs(body.decode())

        task_id = data["id"][0]
        captcha = data["code"][0]

        task_data = tasks.pop(task_id)
        result = await sfr_service.get_regnum(task_data["inn"], task_data["captcha_id"], captcha)
        contact = await bitrix_service.update_contact(task_data["contact_id"], result["regNum"])

    except ContentTypeError as e:
        print(f"Ошибка: {e}, возможно капча не подошла")
