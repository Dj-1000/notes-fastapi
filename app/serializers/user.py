from typing import Union, List
from app.db.models import User

def serialize_user(user: User) -> dict:
    """Serialize a single user instance to dictionary"""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "is_verified": user.is_verified,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }

def serialize_users(data: Union[User, List[User]]) -> Union[dict, List[dict]]:
    """
    Serialize user data - handles both single instance and list of users
    Args:
        data: Single User instance or List of User instances
    Returns:
        Serialized dictionary or list of dictionaries
    """
    if isinstance(data, list):
        return [serialize_user(user) for user in data]
    return serialize_user(data)
