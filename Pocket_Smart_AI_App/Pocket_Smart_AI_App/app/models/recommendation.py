from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    JSON,
    String
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class RecommendationHistory(Base):

    __tablename__ = "recommendation_history"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False
    )

    planner: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    request_data: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    response_data: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )