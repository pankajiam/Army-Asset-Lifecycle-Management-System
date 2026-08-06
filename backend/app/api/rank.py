from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.rank import RankResponse

from app.crud.rank import get_ranks


router = APIRouter(
    prefix="/ranks",
    tags=["Ranks"],
)


@router.get(
    "/",
    response_model=list[RankResponse]
)
def read_ranks(
    db: Session = Depends(get_db)
):

    return get_ranks(db)