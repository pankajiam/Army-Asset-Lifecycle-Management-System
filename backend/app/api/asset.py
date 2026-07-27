from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.database import get_db
from app.schemas.asset import AssetCreate, AssetResponse
from app.crud.asset import create_asset, get_assets

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post("/", response_model=AssetResponse)
def create_new_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db)
):
    return create_asset(db, asset)


@router.get("/", response_model=list[AssetResponse])
def read_assets(
    db: Session = Depends(get_db)
):
    return get_assets(db)