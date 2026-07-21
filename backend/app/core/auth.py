from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings
from app.core.security import verify_password

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def authenticate_user(
    db,
    army_number: str,
    password: str
):
    from app.crud.user import get_user_by_army_number

    user = get_user_by_army_number(
        db,
        army_number
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user