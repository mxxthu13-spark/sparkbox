import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

# 中国时区 UTC+8
CHINA_TZ = timezone(timedelta(hours=8))

def get_china_now():
    """获取中国当前时间"""
    return datetime.now(CHINA_TZ).replace(tzinfo=None)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    wechat_openid: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    nickname: Mapped[str] = mapped_column(String(50), default="闪念用户")
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    ai_provider: Mapped[str] = mapped_column(String(20), default="deepseek")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=get_china_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=get_china_now,
        onupdate=get_china_now,
    )

    thoughts: Mapped[list["Thought"]] = relationship("Thought", back_populates="user", cascade="all, delete-orphan")
    categories: Mapped[list["Category"]] = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="user", cascade="all, delete-orphan")


from models.thought import Thought
from models.category import Category
from models.review import Review
from models.card import Card
