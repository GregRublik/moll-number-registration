from fastapi import APIRouter, Depends, Query
from depends import get_captcha_service, get_sfr_service, get_bitrix_contact_service
from services.bitrix import BitrixContactsService
from services.captcha import CaptchaService
from config import tasks

from services.sfr import SFRService

router = APIRouter(tags=["contacts"], prefix="/contacts")

@router.get("/")
async def get_contacts(
    count: int = Query(),
    contact_service: BitrixContactsService = Depends(get_bitrix_contact_service)
):
    contacts = []

    for i in range(count)[::50]:
        contacts.append(await contact_service.get_contacts(i))
        print(i)
    return contacts

@router.get("/{contact_id}/number/{inn}")
async def create_task_for_registration_number(
    contact_id: int,
    inn: str,
    sfr_service: SFRService = Depends(get_sfr_service),
    captcha_service: CaptchaService = Depends(get_captcha_service),
):
    """Метод ищет регистрационный номер по INN"""
    captcha = await sfr_service.get_captcha()
    captcha_id = captcha["captchaId"]
    task = await captcha_service.create_task(captcha["captchaImage"])

    tasks[str(task["taskId"])] = {"captcha_id": captcha_id, "inn": inn, "contact_id": contact_id}

    return task
