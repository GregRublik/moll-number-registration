from aiohttp import ClientSession
from typing import Literal, Optional

from config import settings
from constants import BitrixContactConstants


class BitrixService:

    def __init__(self, http_session: ClientSession):
        self.http_session = http_session

    async def _request(self, method, url, params, json):
        return await self.http_session.request(
            method=method,
            url=url,
            params=params,
            json=json,
        )

    async def send_request(
        self,
        endpoint: str,
        method: Literal['get', 'post'] = 'post',
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        url = f"{settings.bitrix.webhook_url}/{endpoint}.json"

        response = await self._request(
            method=method,
            url=url,
            params=params,
            json=json
        )

        return await response.json()


class BitrixContactsService(BitrixService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = BitrixContactConstants()

    async def update_contact(self, contact_id: int, number_registration: int):
        contact = await self.send_request(
            "crm.item.update",
            json={
                "entityTypeId": 3,
                "id": contact_id,
                "fields": {
                    self.fields.number_registration: number_registration
                },
                "useOriginalUfNames": "Y"
            }
        )
        return contact

    async def get_contacts(self, start: Optional[int] = 0):
        response = await self.send_request(
            "crm.contact.list",
            json={
                "select": [
                    "ID",
                    "NAME",
                    "SECOND_NAME",
                    "LAST_NAME",
                    self.fields.number_registration,
                    self.fields.inn
                ],
                "filter": {
                    # "ID": "18609",
                    f"={self.fields.number_registration}": "",         # Номер регистрации должен быть не заполнен
                    f"!={self.fields.inn}": ""                         # ИНН должен быть заполнен
                },
                "start": start
            }
        )
        try:
            return response["result"]
        except KeyError:
            print(f"error response: {response}")
            raise
