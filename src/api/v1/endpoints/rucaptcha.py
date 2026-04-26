from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse
from urllib.parse import parse_qs
from config import tasks
from depends import get_sfr_service
from services.sfr import SFRService

router = APIRouter(tags=["rucaptcha"])

@router.get("/rucaptcha.txt")
async def install_webhook():
    return FileResponse(
        "rucaptcha.txt",
    )

@router.post("/callback")
async def callback(
    request: Request,
    sfr_service: SFRService = Depends(get_sfr_service),
):
    body = await request.body()
    data = parse_qs(body.decode())

    task_id = data["id"][0]
    captcha = data["code"][0]

    task_data = tasks.pop(task_id)
    print(task_data)
    result = await sfr_service.get_regnum(task_data["inn"], task_data["captcha_id"], captcha)


    print(result["regNum"])