from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Request, HTTPException
import os
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"

def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)#срок действия (истекает)

    payload = {
        "sub" : str(user_id),
        "exp" : expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def get_current_user(
        request: Request
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return user_id