from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.asset_disposal import (
    DisposalRequest,
    DisposalResponse
)

from app.crud.asset_disposal import (
    request_disposal,
    approve_disposal
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

@router.put(
    "/approve/{disposal_id}",
    response_model=DisposalResponse
)
def approve_disposal_request(
    disposal_id: int,
    approved_by: int,
    db: Session = Depends(get_db)
):
    disposal = approve_disposal(
        db=db,
        disposal_id=disposal_id,
        approved_by=approved_by
    )

    if disposal == "disposal_not_found":
        raise HTTPException(
            status_code=404,
            detail="Disposal request not found"
        )

    if disposal == "already_approved":
        raise HTTPException(
            status_code=400,
            detail="Disposal request already approved"
        )

    if disposal == "approver_not_found":
        raise HTTPException(
            status_code=404,
            detail="Approver not found"
        )

    if disposal == "not_authorized":
        raise HTTPException(
            status_code=403,
            detail="Only Administrator or Commanding Officer can approve disposal requests"
        )

    return disposal