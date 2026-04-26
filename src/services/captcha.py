from aiohttp import ClientSession
from config import settings


class CaptchaService:

    api_key = settings.captcha.api_key
    callback_url = settings.captcha.callback_url
    base_url = "https://api.rucaptcha.com/"

    def __init__(self, http_session: ClientSession):
        self.http_session = http_session

    async def create_task(self, image_b64: str) -> dict:
        url = self.base_url + "createTask"

        response = await self.http_session.post(
            url,
            json={
                "clientKey": self.api_key,
                "task": {
                    "type": "ImageToTextTask",
                    "body": image_b64,
                    "comment": "Введите символы с картинки"
                },
                "languagePool": "rn",
                "callbackUrl": self.callback_url,
            }
        )

        return await response.json()

    async def get_task(self, task_id: str) -> dict:
        url = self.base_url + "getTaskResult"

        response = await self.http_session.post(
            url,
            json={
                "clientKey": self.api_key,
                "taskId": task_id,
            }
        )

        return await response.json()

