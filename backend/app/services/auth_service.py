from sqlalchemy.orm import Session

from app.models.user import User

from app.core.security import (
    verify_password,
    create_access_token,
    decode_access_token,
)

from fastapi import Depends, HTTPException

from fastapi.security import OAuth2PasswordBearer

from app.db.database import get_db


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ============================================================
# LOGIN
# ============================================================

def login_user(
    db: Session,
    email: str,
    password: str
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return "invalid_credentials"

    if not verify_password(
        password,
        user.password_hash
    ):
        return "invalid_credentials"

    token = create_access_token(
        {
            "sub": str(user.user_id)
        }
    )

    return token


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    return user


# ============================================================
# ROLE CHECKING
# ============================================================

def require_roles(*allowed_roles):
    """
    Creates a dependency that allows only users
    whose role is present in allowed_roles.
    """

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if (
            current_user.role is None
            or current_user.role.role_name
            not in allowed_roles
        ):
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action"
            )

        return current_user

    return role_checker


# ============================================================
# COMMON ROLE DEPENDENCIES
# ============================================================

require_admin = require_roles(
    "Administrator"
)


require_admin_or_co = require_roles(
    "Administrator",
    "Commanding Officer"
)


require_inventory_manager = require_roles(
    "Administrator",
    "Commanding Officer",
    "Quarter Master"
)


require_store_manager = require_roles(
    "Administrator",
    "Commanding Officer",
    "Quarter Master",
    "Store Keeper"
)


require_asset_operations = require_roles(
    "Administrator",
    "Commanding Officer",
    "Quarter Master",
    "Store Keeper",
    "Unit Officer"
)