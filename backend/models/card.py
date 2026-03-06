import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    thought_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("thoughts.id", ondelete="SET NULL"), nullable=True
    )
    review_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("reviews.id", ondelete="SET NULL"), nullable=True
    )
    template_id: Mapped[str] = mapped_column(String(50), default="minimal")
    content: Mapped[str] = mapped_column(Text)
    card_config: Mapped[dict] = mapped_column(JSON, default=dict)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="cards")
    thought: Mapped["Thought"] = relationship("Thought", back_populates="cards")
    review: Mapped["Review"] = relationship("Review", back_populates="cards")


from models.user import User
from models.thought import Thought
from models.review import Review
