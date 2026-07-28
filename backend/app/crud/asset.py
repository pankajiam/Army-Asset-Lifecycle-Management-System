from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate

import qrcode
from io import BytesIO

def create_asset(db: Session, asset: AssetCreate):

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
    db.commit()
    db.refresh(db_asset)

    return db_asset


def get_assets(db: Session):
    return db.query(Asset).all()

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