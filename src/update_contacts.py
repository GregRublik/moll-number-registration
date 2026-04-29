import asyncio

from services.bitrix import BitrixContactsService
from config import SessionManager


async def main(count_contacts: int):
    async with await SessionManager().get_session() as session:
        contact_service = BitrixContactsService(session)

        contacts = []
        for i in range(0, count_contacts, 50):  # исправлено: range(start, stop, step)
            contacts += await contact_service.get_contacts(i)
            print(i)

        print(contacts)

        for contact in contacts[:count_contacts]:
            await session.get(f"http://localhost:8000/contacts/{contact['ID']}/number/{contact['UF_CRM_1636582822241']}")

            print("пауза на всякий случай")
            await asyncio.sleep(1)


if __name__ == "__main__":
    count = int(input("Количество контактов: "))
    asyncio.run(main(count))

