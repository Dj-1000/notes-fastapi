ALLOWED_GROUPS = ["admin", "normal_user"]
from app.helpers.auth_helpers import decode_access_token

def check_auth_group(token: str):
    decoded_token = decode_access_token(token)
    if decoded_token and decoded_token.get("group") in ALLOWED_GROUPS:
        return True
    return False

