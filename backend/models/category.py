import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(50))
    icon: Mapped[str] = mapped_column(String(10), default="💡")
    color: Mapped[str] = mapped_column(String(20), default="#6366f1")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_default: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="categories")
    thoughts: Mapped[list["Thought"]] = relationship("Thought", back_populates="category")


DEFAULT_CATEGORIES = [
    {"name": "个人成长", "icon": "🌱", "color": "#10b981"},
    {"name": "育儿", "icon": "👶", "color": "#f59e0b"},
    {"name": "科技思考", "icon": "🔬", "color": "#6366f1"},
    {"name": "日常感悟", "icon": "✨", "color": "#ec4899"},
    {"name": "创意灵感", "icon": "💡", "color": "#f97316"},
    {"name": "工作复盘", "icon": "💼", "color": "#8b5cf6"},
]


from models.user import User
from models.thought import Thought
