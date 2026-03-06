from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func, cast, Date
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from core.database import get_db
from core.security import get_current_user_id
from models.thought import Thought
from models.category import Category
import uuid

router = APIRouter(prefix="/thoughts", tags=["想法"])


class ThoughtCreate(BaseModel):
    content: str
    category_id: Optional[str] = None
    tags: list[str] = []
    mood: Optional[str] = None


class ThoughtUpdate(BaseModel):
    content: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[list[str]] = None
    mood: Optional[str] = None
    is_pinned: Optional[bool] = None


def thought_to_dict(t: Thought, category: Optional[Category] = None) -> dict:
    # 将时间转换为字符串，不使用 isoformat，直接格式化为本地时间字符串
    created_at_str = t.created_at.strftime("%Y-%m-%d %H:%M:%S") if t.created_at else None
    updated_at_str = t.updated_at.strftime("%Y-%m-%d %H:%M:%S") if t.updated_at else None
    
    return {
        "id": t.id,
        "content": t.content,
        "category_id": t.category_id,
        "category": {"id": category.id, "name": category.name, "icon": category.icon, "color": category.color}
        if category
        else None,
        "tags": t.tags or [],
        "mood": t.mood,
        "ai_summary": t.ai_summary,
        "ai_quote": t.ai_quote,
        "is_pinned": t.is_pinned,
        "created_at": created_at_str,
        "updated_at": updated_at_str,
    }


@router.post("/")
async def create_thought(
    body: ThoughtCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    if not body.content.strip():
        raise HTTPException(status_code=400, detail="内容不能为空")

    thought = Thought(
        id=str(uuid.uuid4()),
        user_id=user_id,
        content=body.content.strip(),
        category_id=body.category_id,
        tags=body.tags,
        mood=body.mood,
    )
    db.add(thought)
    await db.commit()
    await db.refresh(thought)

    category = None
    if thought.category_id:
        res = await db.execute(select(Category).where(Category.id == thought.category_id))
        category = res.scalar_one_or_none()

    return thought_to_dict(thought, category)


@router.get("/")
async def list_thoughts(
    category_id: Optional[str] = Query(None),
    category_ids: Optional[str] = Query(None),  # 支持多个分类ID，逗号分隔
    tag: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    is_pinned: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    conditions = [Thought.user_id == user_id, Thought.is_deleted == False]

    if category_id:
        conditions.append(Thought.category_id == category_id)
    elif category_ids:
        # 支持多个分类ID
        cat_id_list = [cid.strip() for cid in category_ids.split(',') if cid.strip()]
        if cat_id_list:
            conditions.append(Thought.category_id.in_(cat_id_list))
    if tag:
        conditions.append(Thought.tags.as_string().contains(tag))
    if search:
        conditions.append(Thought.content.ilike(f"%{search}%"))
    if start_date:
        conditions.append(Thought.created_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        conditions.append(Thought.created_at <= datetime.combine(end_date, datetime.max.time()))
    if is_pinned is not None:
        conditions.append(Thought.is_pinned == is_pinned)

    total_result = await db.execute(
        select(func.count()).select_from(Thought).where(and_(*conditions))
    )
    total = total_result.scalar()

    result = await db.execute(
        select(Thought)
        .where(and_(*conditions))
        .order_by(desc(Thought.is_pinned), desc(Thought.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    thoughts = result.scalars().all()

    category_ids = {t.category_id for t in thoughts if t.category_id}
    categories = {}
    if category_ids:
        cat_result = await db.execute(
            select(Category).where(Category.id.in_(category_ids))
        )
        for cat in cat_result.scalars().all():
            categories[cat.id] = cat

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [thought_to_dict(t, categories.get(t.category_id)) for t in thoughts],
    }


@router.get("/stats/summary")
async def get_stats(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    total = await db.execute(
        select(func.count()).select_from(Thought).where(
            Thought.user_id == user_id, Thought.is_deleted == False
        )
    )
    by_category = await db.execute(
        select(Thought.category_id, func.count().label("count"))
        .where(Thought.user_id == user_id, Thought.is_deleted == False)
        .group_by(Thought.category_id)
    )
    return {
        "total": total.scalar(),
        "by_category": [{"category_id": row[0], "count": row[1]} for row in by_category],
    }


@router.get("/{thought_id}")
async def get_thought(
    thought_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Thought).where(Thought.id == thought_id, Thought.user_id == user_id)
    )
    thought = result.scalar_one_or_none()
    if not thought:
        raise HTTPException(status_code=404, detail="想法不存在")

    category = None
    if thought.category_id:
        res = await db.execute(select(Category).where(Category.id == thought.category_id))
        category = res.scalar_one_or_none()

    return thought_to_dict(thought, category)


@router.put("/{thought_id}")
async def update_thought(
    thought_id: str,
    body: ThoughtUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Thought).where(Thought.id == thought_id, Thought.user_id == user_id)
    )
    thought = result.scalar_one_or_none()
    if not thought:
        raise HTTPException(status_code=404, detail="想法不存在")

    if body.content is not None:
        thought.content = body.content.strip()
    if body.category_id is not None:
        thought.category_id = body.category_id
    if body.tags is not None:
        thought.tags = body.tags
    if body.mood is not None:
        thought.mood = body.mood
    if body.is_pinned is not None:
        thought.is_pinned = body.is_pinned

    await db.commit()
    await db.refresh(thought)

    category = None
    if thought.category_id:
        res = await db.execute(select(Category).where(Category.id == thought.category_id))
        category = res.scalar_one_or_none()

    return thought_to_dict(thought, category)


@router.delete("/{thought_id}")
async def delete_thought(
    thought_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Thought).where(Thought.id == thought_id, Thought.user_id == user_id)
    )
    thought = result.scalar_one_or_none()
    if not thought:
        raise HTTPException(status_code=404, detail="想法不存在")

    thought.is_deleted = True
    await db.commit()
    return {"message": "删除成功"}
