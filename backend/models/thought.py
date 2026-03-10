import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

# 中国时区 UTC+8
CHINA_TZ = timezone(timedelta(hours=8))

def get_china_now():
    """获取中国当前时间（不带时区信息，但是中国时间）"""
    return datetime.now(CHINA_TZ).replace(tzinfo=None)  # UTC+8 时间，去掉时区信息


class Thought(Base):
    __tablename__ = "thoughts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    mood: Mapped[str | None] = mapped_column(String(10), nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_quote: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_pinned: Mapped[bool] = mapped_column(default=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=get_china_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=get_china_now,
        onupdate=get_china_now,
    )

    user: Mapped["User"] = relationship("User", back_populates="thoughts")
    category: Mapped["Category"] = relationship("Category", back_populates="thoughts")
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="thought")


from models.user import User
from models.category import Category
from models.card import Card
