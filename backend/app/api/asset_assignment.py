from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.asset_assignment import (
    AssetIssue,
    AssetReturn,
    AssignmentResponse
)

from app.crud.asset_assignment import (
    issue_asset,
    return_asset
)

router = APIRouter(
    prefix="/assignments",
    tags=["Asset Assignments"]
)


@router.post(
    "/issue",
    response_model=AssignmentResponse
)
def issue(
    request: AssetIssue,
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


@router.post(
    "/return",
    response_model=AssignmentResponse
)
def return_asset_api(
    request: AssetReturn,
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