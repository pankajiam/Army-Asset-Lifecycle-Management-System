from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.rank import RankResponse
from app.crud.rank import get_ranks

from app.models.user import User
from app.services.auth_service import get_current_user


router = APIRouter(
    prefix="/ranks",
    tags=["Ranks"],
)


@router.get(
    "/",
    response_model=list[RankResponse]
)
def read_ranks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_ranks(db)