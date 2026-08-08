from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.asset_status import AssetStatusResponse
from app.crud.asset_status import get_asset_statuses

from app.models.user import User
from app.services.auth_service import get_current_user


router = APIRouter(
    prefix="/asset-status",
    tags=["Asset Status"],
)


@router.get(
    "/",
    response_model=list[AssetStatusResponse]
)
def read_asset_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_asset_statuses(db)