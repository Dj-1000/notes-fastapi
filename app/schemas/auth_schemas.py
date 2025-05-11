from pydantic import BaseModel, EmailStr, constr
from typing import Optional

PhoneNumber = constr(min_length=10, max_length=15)
Password = constr(min_length=6)

class LoginRequest(BaseModel):
    username: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class OTPRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class OTPVerifyRequest(BaseModel):
    otp: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class ForgotPasswordRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class ResetPasswordRequest(BaseModel):
    otp: str
    new_password: str
    confirm_password: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    phone_number: PhoneNumber
    password: Password

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str

    class Config:
        from_attributes = True

class UserDeleteResponse(BaseModel):
    status: str = "success"
    message: str
    data: Optional[dict] = None
    status_code: int

