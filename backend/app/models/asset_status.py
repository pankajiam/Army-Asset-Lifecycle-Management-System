from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AssetStatus(Base):
    __tablename__ = "asset_status"

    status_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    status_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )