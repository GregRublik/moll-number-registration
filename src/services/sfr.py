import base64
from io import BytesIO
from PIL import Image
from aiohttp import ClientSession


class SFRService:

    base_url = "https://ecp.sfr.gov.ru"

    def __init__(self, http_session: ClientSession):
        self.http_session = http_session

    @staticmethod
    def show_captcha(b64):
        img = Image.open(BytesIO(base64.b64decode(b64)))
        img.show()

    async def get_captcha(self) -> dict:
        response = await self.http_session.get(
            f"{self.base_url}/site/captcha",
            headers={
                "User-Agent": "Mozilla/5.0",
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/new-reg-num",
            }
        )
        return await response.json()

        # return data["captchaId"], data["captchaImage"]

    async def get_regnum(self, inn: str, captcha_id: str, captcha, kpp: str = None,) -> dict:

        response = await self.http_session.post(
            f"{self.base_url}/site/regnumsearch",
            headers={
                "User-Agent": "Mozilla/5.0",
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/new-reg-num",
            },
            json={
                "inn": inn,
                "kpp": kpp,
                "capcha": {
                    "captchaAnswer": captcha,
                    "captchaId": captcha_id
                }
            }
        )
        return await response.json()