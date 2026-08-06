from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.unit import UnitResponse

from app.crud.unit import get_units


router = APIRouter(
    prefix="/units",
    tags=["Units"],
)


@router.get(
    "/",
    response_model=list[UnitResponse]
)
def read_units(
    db: Session = Depends(get_db)
):

    return get_units(db)