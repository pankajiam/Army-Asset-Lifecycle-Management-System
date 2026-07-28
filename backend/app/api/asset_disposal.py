from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.asset_disposal import (
    DisposalRequest,
    DisposalResponse
)

from app.crud.asset_disposal import (
    request_disposal
)

router = APIRouter(
    prefix="/disposals",
    tags=["Asset Disposal"]
)


@router.post(
    "/request",
    response_model=DisposalResponse
)
def create_disposal_request(
    request: DisposalRequest,
    db: Session = Depends(get_db)
):
    disposal = request_disposal(
        db=db,
        asset_id=request.asset_id,
        requested_by=request.requested_by,
        reason=request.reason
    )

    if disposal == "asset_not_found":
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    if disposal == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return disposal