from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jose import JWTError


async def jwt_error_handler(request: Request, exc: JWTError) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(JWTError, jwt_error_handler)
    app.add_exception_handler(ValueError, value_error_handler)
