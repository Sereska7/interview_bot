import enum
from datetime import datetime, UTC
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Enum,
    Boolean,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.pkg.models.base_model import Base


class SubscriptionLevel(enum.Enum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"


class Subscription(Base):
    __tablename__ = "subscription"

    subscription_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    level: Mapped[SubscriptionLevel] = mapped_column(
        Enum(SubscriptionLevel, name="subscription_level"),
        default=SubscriptionLevel.FREE,
        nullable=False,
    )

    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="subscription", uselist=False)

    def check_active(self) -> bool:
        """Проверяет, активна ли подписка."""
        if not self.is_active or not self.expires_at:
            return False
        return self.expires_at > datetime.now(UTC)