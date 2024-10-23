from data.models import User
from fastapi import HTTPException
from services.user_service import is_authenticated, from_token, is_admin


def get_user_or_raise_401(token: str) -> User:
    if not is_authenticated(token):
        raise HTTPException(status_code=401)

    return from_token(token)

def verify_authenticated_user(token: str):
    if not is_authenticated(token):
        raise HTTPException(status_code=401)

def verify_admin(token:str):
    if not is_admin(token):
        raise HTTPException(status_code=401)

