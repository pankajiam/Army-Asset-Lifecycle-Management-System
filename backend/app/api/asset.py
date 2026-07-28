from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.schemas.asset import AssetCreate, AssetResponse
from app.crud.asset import (
    create_asset,
    get_assets,
    generate_asset_qr,
    calculate_depreciation
)
from app.models.asset import Asset

from fastapi.responses import StreamingResponse


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

@router.get("/{asset_id}/qr")
def get_asset_qr(
    asset_id: int,
    db: Session = Depends(get_db)
):
    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    qr_image = generate_asset_qr(asset)

    return StreamingResponse(
        qr_image,
        media_type="image/png"
    )

@router.post("/{asset_id}/depreciate")
def depreciate_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    asset = calculate_depreciation(asset)

    db.commit()
    db.refresh(asset)

    return asset