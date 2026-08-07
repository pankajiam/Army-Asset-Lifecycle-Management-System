from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.security import (
    verify_password,
    create_access_token,
)

from app.schemas.auth import TokenResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            (User.email == form_data.username) |
            (User.army_number == form_data.username)
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email/Army Number or password"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email/Army Number or password"
        )

    token = create_access_token(
        {
            "sub": str(user.user_id)
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }