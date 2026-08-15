from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from core.domain.exceptions.expired_token_error import ExpiredTokenError
from core.domain.exceptions.invalid_rulebook_error import InvalidRulebookError
from core.domain.exceptions.invalid_token_error import InvalidTokenError
from core.domain.exceptions.missing_token_error import MissingTokenError
from core.domain.exceptions.revoked_token_error import RevokedTokenError
from core.domain.exceptions.rulebook_not_found_error import RulebookNotFoundError
from core.domain.exceptions.rulebook_not_processed import RulebookNotProcessed
from core.domain.exceptions.rulebook_processing_failed import RulebookProcessingFailed
from core.domain.exceptions.session_not_found_error import SessionNotFoundError


def exception_container(app: FastAPI) -> None:
    @app.exception_handler(MissingTokenError)
    async def missing_token_handler(
        request: Request, exc: MissingTokenError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(exc)}
        )

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(
        request: Request, exc: InvalidTokenError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(exc)}
        )

    @app.exception_handler(ExpiredTokenError)
    async def expired_token_handler(
        request: Request, exc: ExpiredTokenError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(exc)}
        )

    @app.exception_handler(RevokedTokenError)
    async def revoked_token_handler(
        request: Request, exc: RevokedTokenError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(exc)}
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )

    @app.exception_handler(RulebookNotFoundError)
    async def rulebook_not_found_handler(
        request: Request, exc: RulebookNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )

    @app.exception_handler(SessionNotFoundError)
    async def session_not_found_handler(
        request: Request, exc: SessionNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )

    @app.exception_handler(InvalidRulebookError)
    async def invalid_rulebook_handler(
        request: Request, exc: InvalidRulebookError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)}
        )
