from fastapi import FastAPI
from api.v1.endpoints import main, rucaptcha
import uvicorn

from config import settings

app = FastAPI()

app.include_router(main.router)
app.include_router(rucaptcha.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
