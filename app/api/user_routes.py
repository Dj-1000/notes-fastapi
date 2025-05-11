from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sqlalchemy.exc
from app.db.database import get_db
from app.schemas.auth_schemas import UserOut, UserCreate
from app.services.auth_service import get_current_user
from app.db import models
import bcrypt
from app.schemas.response_schemas import error_response, success_response, SuccessResponse
from app.db.models import User
from app.serializers.user import serialize_users
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def create_user(user_create, session):
    try:
        user = User(
            username=user_create.email,
            email=user_create.email,
            phone=user_create.phone_number,
            password=user_create.password
        )
        session.add(user)
        session.commit()
        return serialize_users(user)
    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Duplicate entry")
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail="Error occurred while creating user")

@router.post("/")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        (models.User.email == user_data.email) 
    ).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists with same details.")

    # Hash password
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data.password = hashed_password

    user = create_user(user_data, db)
    return success_response("User created successfully.", user)

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    db.delete(user)
    db.commit()
    return {
        "status": "success",
        "message": f"User with ID {user_id} deleted.",
        "data": None,
        "status_code": 200
    }
