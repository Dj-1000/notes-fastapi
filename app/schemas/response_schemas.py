from pydantic import BaseModel
from typing import Any, List, Union

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str
    data: Union[Any, None] = None
    status_code: int

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    errors: Union[List[Union[str, dict]], None] = None
    status_code: int


def success_response(message: str, data: Any = None):
    return SuccessResponse(message=message, data=data, status_code=200)

def error_response(message: str, errors: List[Union[str, dict]] = None, status_code: int = 400):
    return ErrorResponse(message=message, errors=errors, status_code=status_code)

