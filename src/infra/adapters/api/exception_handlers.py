from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from core.domain.exceptions.session_not_found_error import SessionNotFoundError


def exception_container(app: FastAPI) -> None:
    @app.exception_handler(SessionNotFoundError)
    async def session_not_found_exception_handler(request: Request, exc: SessionNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"message": str(exc)}
        )