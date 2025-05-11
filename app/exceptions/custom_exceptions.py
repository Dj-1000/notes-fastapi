from fastapi import HTTPException
from app.schemas.response_schemas import ErrorResponse
class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid credentials.")

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found.")

class OTPMismatchException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid or expired OTP.")

class ValidationError(HTTPException):
    def __init__(self, errors: list):
        super().__init__(
            status_code=400,
            detail=ErrorResponse(
                status="error",
                message="Validation Error",
                errors=errors,
                status_code=400
            ).model_dump()
        )

