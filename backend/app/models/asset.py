from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Numeric,
    Boolean
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)

    asset_code = Column(String(50), unique=True, nullable=False)

    asset_name = Column(String(200), nullable=False)

    category = Column(String(100), nullable=False)

    manufacturer = Column(String(100))

    model = Column(String(100))

    serial_number = Column(String(100), unique=True)

    purchase_date = Column(Date)

    purchase_price = Column(Numeric(12,2))

    current_value = Column(Numeric(12,2))

    status = Column(
        String(30),
        default="Available"
    )

    qr_code = Column(String(255))

    assigned_to = Column(
    Integer,
    ForeignKey("users.user_id"),
    nullable=True
    )
    is_active = Column(
        Boolean,
        default=True
    )

    owner = relationship("User")