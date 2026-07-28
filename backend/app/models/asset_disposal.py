from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class AssetDisposal(Base):
    __tablename__ = "asset_disposals"

    disposal_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    asset_id = Column(
        Integer,
        ForeignKey("assets.asset_id"),
        nullable=False
    )

    requested_by = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    approved_by = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=True
    )

    reason = Column(
        String(255),
        nullable=False
    )

    status = Column(
        String(50),
        default="Pending"
    )

    requested_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    approved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    asset = relationship("Asset")