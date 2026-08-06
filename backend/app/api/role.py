from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.role import RoleResponse

from app.crud.role import get_roles


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.get(
    "/",
    response_model=list[RoleResponse]
)
def read_roles(
    db: Session = Depends(get_db)
):

    return get_roles(db)