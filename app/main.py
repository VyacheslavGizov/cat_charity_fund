from fastapi import FastAPI

from app.api.routers import main_router
from app.core.init_db import create_first_superuser
from app.core.config import settings, APP_TITLE, APP_DECRIPTION


app = FastAPI(title=APP_TITLE, description=APP_DECRIPTION)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
