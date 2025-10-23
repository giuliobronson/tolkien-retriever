from fastapi import FastAPI

from adapters.api.exception_handlers import exception_container
from adapters.api.routers import session
from adapters.api.routers import chat


app = FastAPI()

app.include_router(chat.router)
app.include_router(session.router)

exception_container(app)