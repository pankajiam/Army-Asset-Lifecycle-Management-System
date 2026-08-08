from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.asset_assignment import (
    AssetIssue,
    AssetReturn,
    AssetTransfer,
    AssignmentResponse,
)

from app.crud.asset_assignment import (
    issue_asset,
    return_asset,
    transfer_asset,
    get_asset_history,
    get_assignments,
)

from app.models.user import User

from app.services.auth_service import (
    require_asset_operations,
)


router = APIRouter(
    prefix="/assignments",
    tags=["Asset Assignments"]
)


# ============================================================
# LIST ALL ASSIGNMENTS
# All authenticated users
# ============================================================

@router.get(
    "/",
    response_model=list[AssignmentResponse]
)
def list_assignments(
    current_user: User = Depends(require_asset_operations),
    db: Session = Depends(get_db)
):
    return get_assignments(db)


# ============================================================
# ISSUE ASSET
# Administrator / CO / Quarter Master / Store Keeper
# ============================================================

@router.post(
    "/issue",
    response_model=AssignmentResponse
)
def issue(
    request: AssetIssue,
    current_user: User = Depends(require_asset_operations),
    db: Session = Depends(get_db)
):
    assignment = issue_asset(
        db=db,
        asset_id=request.asset_id,
        user_id=request.user_id,
        issue_condition=request.issue_condition
    )

    if assignment is None:
        raise HTTPException(
            status_code=404,
            detail="Asset or User not found"
        )

    if assignment == "already_assigned":
        raise HTTPException(
            status_code=400,
            detail="Asset is already assigned"
        )

    return assignment


# ============================================================
# RETURN ASSET
# Administrator / CO / Quarter Master / Store Keeper
# ============================================================

@router.post(
    "/return",
    response_model=AssignmentResponse
)
def return_asset_api(
    request: AssetReturn,
    current_user: User = Depends(require_asset_operations),
    db: Session = Depends(get_db)
):
    assignment = return_asset(
        db=db,
        asset_id=request.asset_id,
        return_condition=request.return_condition
    )

    if assignment is None:
        raise HTTPException(
            status_code=404,
            detail="No active assignment found"
        )

    return assignment


# ============================================================
# TRANSFER ASSET
# Administrator / CO / Quarter Master / Store Keeper
# ============================================================

@router.post(
    "/transfer",
    response_model=AssignmentResponse
)
def transfer_asset_api(
    request: AssetTransfer,
    current_user: User = Depends(require_asset_operations),
    db: Session = Depends(get_db)
):
    assignment = transfer_asset(
        db=db,
        asset_id=request.asset_id,
        new_user_id=request.new_user_id,
        transfer_condition=request.transfer_condition
    )

    if assignment is None:
        raise HTTPException(
            status_code=404,
            detail="No active assignment found"
        )

    if assignment == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="New user not found"
        )

    if assignment == "same_user":
        raise HTTPException(
            status_code=400,
            detail="Asset is already assigned to this user"
        )

    return assignment


# ============================================================
# ASSET ASSIGNMENT HISTORY
# All authenticated users
# ============================================================

@router.get(
    "/history/{asset_id}",
    response_model=list[AssignmentResponse]
)
def asset_history(
    asset_id: int,
    current_user: User = Depends(require_asset_operations),
    db: Session = Depends(get_db)
):
    return get_asset_history(
        db=db,
        asset_id=asset_id
    )