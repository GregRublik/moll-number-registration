from fastapi import FastAPI
from api.v1.endpoints import contacts, rucaptcha
import uvicorn

from config import settings

app = FastAPI()

# app.include_router(captcha.router)
app.include_router(rucaptcha.router)
app.include_router(contacts.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
