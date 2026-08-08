from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.unit import UnitResponse
from app.crud.unit import get_units

from app.models.user import User
from app.services.auth_service import get_current_user


router = APIRouter(
    prefix="/units",
    tags=["Units"],
)


@router.get(
    "/",
    response_model=list[UnitResponse]
)
def read_units(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_units(db)