from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth_schemas import (
    LoginRequest, OTPVerifyRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.services import auth_service, otp_service, email_service, twilio_service
from app.schemas.response_schemas import SuccessResponse, ErrorResponse
from app.exceptions.custom_exceptions import ValidationError
from app.db.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=SuccessResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_with_credentials(data, db)

@router.post("/verify-login", response_model=SuccessResponse)
def verify_login(data: OTPVerifyRequest, db: Session = Depends(get_db)):
    return auth_service.verify_login_otp(data.email or data.phone, data.otp, db)

@router.post("/forgot-password", response_model=SuccessResponse)
def forgot_password(data: ForgotPasswordRequest):
    otp = otp_service.generate_otp(data.email or data.phone)
    if data.email:
        email_service.send_email(data.email, "Password Reset OTP", f"Your OTP is {otp}")
    elif data.phone:
        twilio_service.send_sms(data.phone, f"Your OTP is {otp}")
    else:
        raise ValidationError([{"field": "email", "error": "Email or phone required."}])
    return {
        "status": "success",
        "message": "OTP sent successfully.",
        "status_code": 200
    }

@router.post("/reset-password", response_model=SuccessResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    key = data.email or data.phone
    if not otp_service.verify_otp(key, data.otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    user = None
    if data.email:
        user = db.query(User).filter_by(email=data.email).first()
    elif data.phone:
        user = db.query(User).filter_by(phone=data.phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.password = data.new_password
    db.commit()
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {
        "status": "success",
        "message": "Password reset successful.",
        "data": {"access_token": access_token, "token_type": "bearer"},
        "status_code": 200
    }