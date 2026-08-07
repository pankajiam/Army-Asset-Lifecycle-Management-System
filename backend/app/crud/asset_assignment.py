from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.asset import Asset
from app.models.user import User
from app.models.asset_assignment import AssetAssignment


def _assignment_response(assignment: AssetAssignment):
    return {
        "assignment_id": assignment.assignment_id,

        "asset_id": assignment.asset_id,
        "asset_name": assignment.asset.asset_name,

        "user_id": assignment.user_id,
        "user_name": f"{assignment.user.first_name} {assignment.user.last_name}",

        "issued_at": assignment.issued_at,
        "issue_condition": assignment.issue_condition,
        "return_condition": assignment.return_condition,
        "returned_at": assignment.returned_at,
    }


def issue_asset(
    db: Session,
    asset_id: int,
    user_id: int,
    issue_condition: str
):
    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id)
        .first()
    )

    if not asset:
        return None

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
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

    return _assignment_response(assignment)


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
        .filter(Asset.asset_id == asset_id)
        .first()
    )

    assignment.returned_at = func.now()
    assignment.return_condition = return_condition

    asset.status = "Available"

    db.commit()
    db.refresh(assignment)

    return _assignment_response(assignment)


def transfer_asset(
    db: Session,
    asset_id: int,
    new_user_id: int,
    transfer_condition: str
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

    new_user = (
        db.query(User)
        .filter(User.user_id == new_user_id)
        .first()
    )

    if not new_user:
        return "user_not_found"

    if assignment.user_id == new_user_id:
        return "same_user"

    assignment.returned_at = func.now()
    assignment.return_condition = transfer_condition

    new_assignment = AssetAssignment(
        asset_id=asset_id,
        user_id=new_user_id,
        issue_condition=transfer_condition
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return _assignment_response(new_assignment)


def get_asset_history(
    db: Session,
    asset_id: int
):
    history = (
        db.query(AssetAssignment)
        .filter(
            AssetAssignment.asset_id == asset_id
        )
        .order_by(
            AssetAssignment.issued_at
        )
        .all()
    )

    return [_assignment_response(item) for item in history]


def get_assignments(db: Session):

    assignments = (
        db.query(AssetAssignment)
        .order_by(
            AssetAssignment.issued_at.desc()
        )
        .all()
    )

    return [_assignment_response(item) for item in assignments]