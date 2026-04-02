from fastapi import FastAPI

import config
from infra.drivers.api.exception_handlers import exception_container
from infra.drivers.api.routers import chat, rulebook, session

app = FastAPI()

app.include_router(chat.router, prefix="/api/v1")
app.include_router(session.router, prefix="/api/v1")
app.include_router(rulebook.router, prefix="/api/v1")

exception_container(app)
