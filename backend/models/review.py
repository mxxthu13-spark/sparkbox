import uuid
from datetime import datetime, timezone, date
from sqlalchemy import String, DateTime, ForeignKey, Text, JSON, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    period_type: Mapped[str] = mapped_column(String(10))  # "week" | "month" | "custom"
    period_start: Mapped[date] = mapped_column(Date)
    period_end: Mapped[date] = mapped_column(Date)
    title: Mapped[str] = mapped_column(String(100))
    thought_ids: Mapped[list] = mapped_column(JSON, default=list)
    thought_count: Mapped[int] = mapped_column(default=0)
    category_ids: Mapped[list] = mapped_column(JSON, default=list)  # 涉及的分类ID列表
    theme: Mapped[str | None] = mapped_column(String(200), nullable=True)  # 回顾主题
    review_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)  # 回顾模式: summary/insight/soul
    ai_content: Mapped[str | None] = mapped_column(Text, nullable=True)  # AI生成的完整内容
    ai_insights: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_keywords: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="reviews")
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="review")


from models.user import User
from models.card import Card
