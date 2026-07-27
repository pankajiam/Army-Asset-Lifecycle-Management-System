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


class AssetAssignment(Base):
    __tablename__ = "asset_assignments"

    assignment_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    asset_id = Column(
        Integer,
        ForeignKey("assets.asset_id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    issued_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    returned_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    issue_condition = Column(
        String(100),
        default="Good"
    )

    return_condition = Column(
        String(100),
        nullable=True
    )

    asset = relationship("Asset")
    user = relationship("User")