from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.audit_log import AuditLog
from app.schemas.asset import AssetCreate

from app.crud.audit_log import create_audit_log

import qrcode
from io import BytesIO

from datetime import date


def create_asset(db: Session, asset: AssetCreate):

    try:

        db_asset = Asset(
            asset_code=asset.asset_code,
            asset_name=asset.asset_name,
            category=asset.category,
            manufacturer=asset.manufacturer,
            model=asset.model,
            serial_number=asset.serial_number,
            purchase_date=asset.purchase_date,
            purchase_price=asset.purchase_price,
            current_value=asset.current_value,
            status=asset.status,
            assigned_to=asset.assigned_to,
        )

        db.add(db_asset)

        db.flush()

        create_audit_log(
            db=db,
            user_id=50,
            asset_id=db_asset.asset_id,
            action="Asset Created",
            remarks=f"{db_asset.asset_name} created"
        )

        db.commit()

        db.refresh(db_asset)

        return db_asset

    except Exception:
        db.rollback()
        raise


def get_assets(db: Session):
    return db.query(Asset).all()


def update_asset(
    db: Session,
    asset_id: int,
    updated_asset: AssetCreate,
):

    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id)
        .first()
    )

    if not asset:
        return None

    asset.asset_code = updated_asset.asset_code
    asset.asset_name = updated_asset.asset_name
    asset.category = updated_asset.category
    asset.manufacturer = updated_asset.manufacturer
    asset.model = updated_asset.model
    asset.serial_number = updated_asset.serial_number
    asset.purchase_date = updated_asset.purchase_date
    asset.purchase_price = updated_asset.purchase_price
    asset.current_value = updated_asset.current_value
    asset.status = updated_asset.status
    asset.assigned_to = updated_asset.assigned_to

    create_audit_log(
        db=db,
        user_id=50,
        asset_id=asset.asset_id,
        action="Asset Updated",
        remarks=f"{asset.asset_name} updated"
    )

    db.commit()

    db.refresh(asset)

    return asset


def delete_asset(
    db: Session,
    asset_id: int,
):

    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id)
        .first()
    )

    if not asset:
        return "NOT_FOUND"

    audit_logs = (
    db.query(AuditLog)
    .filter(AuditLog.asset_id == asset_id)
    .all()
    )

    if len(audit_logs) > 1:
        return "HAS_HISTORY"

    if len(audit_logs) == 1:

        if audit_logs[0].action != "Asset Created":
            return "HAS_HISTORY"

    for log in audit_logs:
        db.delete(log)

    db.delete(asset)

    db.commit()

    return "DELETED"


def generate_asset_qr(asset):

    qr_data = (
        f"Asset ID: {asset.asset_id}\n"
        f"Asset Code: {asset.asset_code}\n"
        f"Asset Name: {asset.asset_name}\n"
        f"Serial Number: {asset.serial_number}\n"
        f"Status: {asset.status}"
    )

    img = qrcode.make(qr_data)

    buffer = BytesIO()

    img.save(buffer, format="PNG")

    buffer.seek(0)

    return buffer


def calculate_depreciation(asset):

    today = date.today()

    years = today.year - asset.purchase_date.year

    depreciation_rate = 0.10

    current_value = (
        float(asset.purchase_price)
        * ((1 - depreciation_rate) ** years)
    )

    asset.current_value = round(current_value, 2)

    return asset