from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class AssetCreate(BaseModel):
    asset_code: str
    asset_name: str
    category: str
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    purchase_date: date | None = None
    purchase_price: Decimal | None = None
    current_value: Decimal | None = None
    status: str = "Available"
    assigned_to: int | None = None


class AssetResponse(AssetCreate):
    asset_id: int

    class Config:
        from_attributes = True