from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "message": exc.detail,
            "errors": [exc.detail],
            "status_code": exc.status_code
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": err["loc"], "error": err["msg"]} for err in exc.errors()]
    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "message": "Validation Error",
            "errors": errors,
            "status_code": 422
        },
    )
