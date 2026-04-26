from fastapi import APIRouter, Depends
from depends import get_captcha_service, get_sfr_service
from services.captcha import CaptchaService
from config import tasks

from services.sfr import SFRService

router = APIRouter(tags=["main"])

@router.get("/get_number/{inn}")
async def get_number(
    inn: str,
    sfr_service: SFRService = Depends(get_sfr_service),
    captcha_service: CaptchaService = Depends(get_captcha_service),
):
    captcha = await sfr_service.get_captcha()
    captcha_id = captcha["captchaId"]
    task = await captcha_service.create_task(captcha["captchaImage"])

    tasks[str(task["taskId"])] = {"captcha_id": captcha_id, "inn": inn}

    return task

@router.get("/get_res_task/{task_id}")
async def get_task(
    task_id: str,
    captcha_service: CaptchaService = Depends(get_captcha_service),
):
    return await captcha_service.get_task(task_id)

