from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.user import User
from app.models.asset_disposal import AssetDisposal
from app.crud.audit_log import create_audit_log

def request_disposal(
    db: Session,
    asset_id: int,
    requested_by: int,
    reason: str
):
    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id)
        .first()
    )

    if not asset:
        return "asset_not_found"

    user = (
        db.query(User)
        .filter(User.user_id == requested_by)
        .first()
    )

    if not user:
        return "user_not_found"

    disposal = AssetDisposal(
        asset_id=asset_id,
        requested_by=requested_by,
        reason=reason
    )

    asset.status = "Pending Disposal"

    db.add(disposal)
    db.commit()
    db.refresh(disposal)

    return disposal

def approve_disposal(
    db: Session,
    disposal_id: int,
    approved_by: int
):
    disposal = (
        db.query(AssetDisposal)
        .filter(AssetDisposal.disposal_id == disposal_id)
        .first()
    )

    if not disposal:
        return "disposal_not_found"

    if disposal.status == "Approved":
        return "already_approved"

    approver = (
        db.query(User)
        .filter(User.user_id == approved_by)
        .first()
    )

    if not approver:
        return "approver_not_found"

    if approver.role.role_name not in [
        "Administrator",
        "Commanding Officer"
    ]:
        return "not_authorized"

    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == disposal.asset_id)
        .first()
    )

    disposal.status = "Approved"
    disposal.approved_by = approved_by

    asset.status = "Disposed"

    db.commit()
    db.refresh(disposal)

    create_audit_log(
        db=db,
        user_id=approved_by,
        asset_id=asset.asset_id,
        action="Approved Disposal",
        remarks=disposal.reason
    )

    return disposal