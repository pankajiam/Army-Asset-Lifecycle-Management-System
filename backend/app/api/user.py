from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user

from fastapi import HTTPException
from app.schemas.login import LoginRequest, Token
from app.core.auth import authenticate_user, create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        login_data.army_number,
        login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Army Number or Password"
        )

    access_token = create_access_token(
        {"sub": user.army_number}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }