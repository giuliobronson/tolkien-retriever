from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from core.domain.exceptions.rulebook_not_processed import RulebookNotProcessed
from core.domain.exceptions.rulebook_processing_failed import RulebookProcessingFailed
from core.domain.exceptions.session_not_found_error import SessionNotFoundError


def exception_container(app: FastAPI) -> None:
    @app.exception_handler(SessionNotFoundError)
    async def session_not_found_exception_handler(
        request: Request, exc: SessionNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )

    @app.exception_handler(RulebookNotProcessed)
    async def rulebook_not_processed_exception_handler(
        request: Request, exc: RulebookNotProcessed
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"message": str(exc)}
        )
    
    @app.exception_handler(RulebookProcessingFailed)
    async def rulebook_processing_failed_handler(
        request: Request, exc: RulebookProcessingFailed
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(exc)}
        )
