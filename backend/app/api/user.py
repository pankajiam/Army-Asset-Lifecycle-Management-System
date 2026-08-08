from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.schemas.login import (
    LoginRequest,
    Token,
)

from app.crud.user import (
    create_user,
    get_users,
)

from app.core.auth import (
    authenticate_user,
    create_access_token,
)

from app.services.auth_service import (
    get_current_user,
    require_admin_or_co,
)

from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ============================================================
# CREATE USER
# Administrator + Commanding Officer only
# ============================================================

@router.post(
    "/",
    response_model=UserResponse
)
def create_new_user(
    user: UserCreate,
    current_user: User = Depends(require_admin_or_co),
    db: Session = Depends(get_db)
):
    return create_user(
        db,
        user
    )


# ============================================================
# GET ALL USERS
# Administrator + Commanding Officer only
# ============================================================

@router.get(
    "/",
    response_model=list[UserResponse]
)
def read_users(
    current_user: User = Depends(require_admin_or_co),
    db: Session = Depends(get_db)
):
    return get_users(db)


# ============================================================
# LOGIN
# Existing login preserved
# ============================================================

@router.post(
    "/login",
    response_model=Token
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        login_data.army_number,
        login_data.password,
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Army Number or Password",
        )

    access_token = create_access_token(
        {
            "sub": str(user.user_id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }