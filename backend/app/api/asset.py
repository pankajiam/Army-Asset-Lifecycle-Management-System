from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi.responses import StreamingResponse

from app.db.database import get_db

from app.schemas.asset import (
    AssetCreate,
    AssetResponse,
)

from app.models.asset import Asset
from app.models.user import User

from app.crud.asset import (
    create_asset,
    get_assets,
    update_asset,
    delete_asset,
    generate_asset_qr,
    calculate_depreciation,
)

from app.services.auth_service import (
    require_asset_operations,
    require_store_manager,
    require_admin,
)


router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


# ============================================================
# CREATE ASSET
# Administrator / CO / Quarter Master / Store Keeper
# ============================================================

@router.post(
    "/",
    response_model=AssetResponse
)
def create_new_asset(
    asset: AssetCreate,
    current_user: User = Depends(require_store_manager),
    db: Session = Depends(get_db)
):
    try:

        return create_asset(
            db,
            asset
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Asset Code or Serial Number already exists."
        )


# ============================================================
# VIEW ASSETS
# All authenticated roles
# ============================================================

@router.get(
    "/",
    response_model=list[AssetResponse]
)
def read_assets(
    current_user: User = Depends(require_asset_operations),
    db: Session = Depends(get_db)
):
    return get_assets(db)


# ============================================================
# EDIT ASSET
# Administrator / CO / Quarter Master / Store Keeper
# ============================================================

@router.put(
    "/{asset_id}",
    response_model=AssetResponse
)
def edit_asset(
    asset_id: int,
    asset: AssetCreate,
    current_user: User = Depends(require_store_manager),
    db: Session = Depends(get_db)
):

    try:

        updated = update_asset(
            db,
            asset_id,
            asset,
        )

        if updated is None:

            raise HTTPException(
                status_code=404,
                detail="Asset not found"
            )

        return updated

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Asset Code or Serial Number already exists."
        )


# ============================================================
# DELETE ASSET
# Administrator ONLY
# ============================================================

@router.delete(
    "/{asset_id}"
)
def remove_asset(
    asset_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):

    result = delete_asset(
        db,
        asset_id,
    )

    if result == "NOT_FOUND":

        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    if result == "HAS_HISTORY":

        raise HTTPException(
            status_code=400,
            detail=(
                "This asset has historical records and cannot be deleted. "
                "Use Disposal instead."
            )
        )

    return {
        "message": "Asset deleted successfully"
    }


# ============================================================
# GENERATE / VIEW ASSET QR
# All authenticated roles
# ============================================================

@router.get(
    "/{asset_id}/qr"
)
def get_asset_qr(
    asset_id: int,
    current_user: User = Depends(require_asset_operations),
    db: Session = Depends(get_db)
):

    asset = (
        db.query(Asset)
        .filter(
            Asset.asset_id == asset_id
        )
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


# ============================================================
# DEPRECIATE ASSET
# Administrator / CO / Quarter Master / Store Keeper
# ============================================================

@router.post(
    "/{asset_id}/depreciate"
)
def depreciate_asset(
    asset_id: int,
    current_user: User = Depends(require_store_manager),
    db: Session = Depends(get_db)
):

    asset = (
        db.query(Asset)
        .filter(
            Asset.asset_id == asset_id
        )
        .first()
    )

    if not asset:

        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    asset = calculate_depreciation(
        asset
    )

    db.commit()

    db.refresh(asset)

    return asset