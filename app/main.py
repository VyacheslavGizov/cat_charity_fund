from fastapi import FastAPI

from app.api.routers import main_router


app = FastAPI()  # Добавить заголовок и описание

app.include_router(main_router)
