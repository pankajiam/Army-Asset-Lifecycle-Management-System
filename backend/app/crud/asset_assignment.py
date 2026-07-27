from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.user import User
from app.models.asset_assignment import AssetAssignment


def issue_asset(
    db: Session,
    asset_id: int,
    user_id: int,
    issue_condition: str
):
    asset = (
        db.query(Asset)
        .filter(
            Asset.asset_id == asset_id
        )
        .first()
    )

    if not asset:
        return None

    user = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )

    if not user:
        return None

    existing = (
        db.query(AssetAssignment)
        .filter(
            AssetAssignment.asset_id == asset_id,
            AssetAssignment.returned_at == None
        )
        .first()
    )

    if existing:
        return "already_assigned"

    assignment = AssetAssignment(
        asset_id=asset_id,
        user_id=user_id,
        issue_condition=issue_condition
    )

    asset.status = "Issued"

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


from sqlalchemy.sql import func


def return_asset(
    db: Session,
    asset_id: int,
    return_condition: str
):
    assignment = (
        db.query(AssetAssignment)
        .filter(
            AssetAssignment.asset_id == asset_id,
            AssetAssignment.returned_at == None
        )
        .first()
    )

    if not assignment:
        return None

    asset = (
        db.query(Asset)
        .filter(
            Asset.asset_id == asset_id
        )
        .first()
    )

    assignment.returned_at = func.now()
    assignment.return_condition = return_condition

    asset.status = "Available"

    db.commit()
    db.refresh(assignment)

    return assignment