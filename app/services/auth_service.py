from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import get_db
from app.helpers.auth_helpers import create_access_token
from app.schemas.auth_schemas import LoginRequest
from app.services.otp_service import generate_otp, verify_otp
from app.services.email_service import send_email
from app.services.twilio_service import send_sms
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.schemas.response_schemas import error_response
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def login_with_credentials(data: LoginRequest, db: Session):
    if data.username:
        user = db.query(models.User).filter_by(username=data.username).first()
    elif data.phone:
        user = db.query(models.User).filter_by(phone=data.phone).first()
    else:
        raise HTTPException(status_code=400, detail="Username or phone required.")

    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # Send email verification
    otp = generate_otp(user,db)
    send_email(user.email, "Your Login OTP", f"Your OTP is {otp}")

    return {
        "status": "success",
        "message": "OTP sent to your email.",
        "status_code": 200
    }

def verify_login_otp(email: str, otp: str, db: Session):
    if verify_otp(email, otp, db):
        user = db.query(models.User).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        access_token = create_access_token(data={"sub": user.username})
        return {
            "status": "success",
            "message": "Login successful.",
            "data": {"access_token": access_token, "token_type": "bearer"},
            "status_code": 200
        }
    raise HTTPException(status_code=400, detail="Invalid or expired OTP.")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return error_response("User not found.", status_code=404)
    except JWTError:
        return error_response("Invalid token.", status_code=401)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return error_response("User not found.", status_code=404)

    return user