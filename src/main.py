from fastapi import FastAPI

from infra.adapters.api.exception_handlers import exception_container
from infra.adapters.api.routers import chat, session


app = FastAPI()

app.include_router(chat.router)
app.include_router(session.router)

exception_container(app)