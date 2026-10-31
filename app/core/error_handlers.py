import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError


logger = logging.getLogger(__name__)


def error_body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    # Erros previstos: devolvemos a mensagem da própria exceção.
    return JSONResponse(
        status_code=exc.status_code,
        content=error_body(exc.code, exc.message),
    )


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    # Erros imprevistos (ex.: base de dados em baixo): registamos o detalhe no log,
    # mas ao utilizador só vai uma mensagem genérica — nada de stack traces ou SQL.
    logger.exception("Erro inesperado em %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=error_body(AppError.code, AppError.message),
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)
