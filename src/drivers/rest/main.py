from fastapi import FastAPI

from drivers.rest.routers import chat


app = FastAPI()

app.include_router(chat.router)