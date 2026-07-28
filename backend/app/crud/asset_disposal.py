from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.user import User
from app.models.asset_disposal import AssetDisposal


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