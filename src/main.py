from fastapi import FastAPI

from infra.drivers.api.exception_handlers import exception_container
from infra.drivers.api.routers import chat, rulebook, session

app = FastAPI()

app.include_router(chat.router)
app.include_router(session.router)
app.include_router(rulebook.router)

exception_container(app)
