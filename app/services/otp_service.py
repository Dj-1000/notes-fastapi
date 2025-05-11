import random
import time
from app.db.models import OTP, User
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.core.config import settings


def generate_otp(user: User, db: Session) -> str:
    otp = str(random.randint(100000, 999999))
    if db.query(OTP).filter_by(email=user.email).first():
        db.query(OTP).filter_by(email=user.email).delete()
    db.add(OTP(email=user.email, otp=otp, created_at=datetime.now(timezone.utc)))
    db.commit()
    return otp

def verify_otp(email: str, otp: str, db: Session, ttl_seconds=settings.OTP_TTL) -> bool:
    stored_otp = db.query(OTP).filter_by(email=email).first()
    if stored_otp and stored_otp.otp == otp and datetime.now() < stored_otp.created_at + timedelta(seconds=ttl_seconds):
        db.delete(stored_otp)
        db.commit()
        return True
    return False
