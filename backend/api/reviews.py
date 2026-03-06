from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
from pydantic import BaseModel
from typing import Optional
from datetime import date, timedelta, datetime, timezone, time
from core.database import get_db
from core.security import get_current_user_id
from models.review import Review
from models.thought import Thought
import uuid

router = APIRouter(prefix="/reviews", tags=["回顾"])


class ReviewCreate(BaseModel):
    period_type: str = "week"  # week | month | custom
    period_start: date
    period_end: date
    title: Optional[str] = None
    category_ids: Optional[list[str]] = None
    theme: Optional[str] = None
    review_mode: Optional[str] = None  # summary/insight/soul
    ai_content: Optional[str] = None  # AI生成的完整内容


class ReviewUpdate(BaseModel):
    ai_insights: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_keywords: Optional[list[str]] = None


def review_to_dict(r: Review) -> dict:
    return {
        "id": r.id,
        "period_type": r.period_type,
        "period_start": r.period_start.isoformat() if r.period_start else None,
        "period_end": r.period_end.isoformat() if r.period_end else None,
        "title": r.title,
        "thought_count": r.thought_count,
        "category_ids": r.category_ids or [],
        "theme": r.theme,
        "review_mode": r.review_mode,
        "ai_content": r.ai_content,
        "ai_insights": r.ai_insights,
        "ai_summary": r.ai_summary,
        "ai_keywords": r.ai_keywords or [],
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }


@router.post("/generate")
async def generate_review(
    body: ReviewCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    # 构建查询条件
    conditions = [
        Thought.user_id == user_id,
        Thought.is_deleted == False,
        Thought.created_at >= datetime.combine(body.period_start, time.min),
        Thought.created_at <= datetime.combine(body.period_end, time.max),
    ]
    
    # 如果指定了分类，只查询这些分类的想法
    if body.category_ids and len(body.category_ids) > 0:
        conditions.append(Thought.category_id.in_(body.category_ids))
    
    thoughts_result = await db.execute(
        select(Thought).where(and_(*conditions)).order_by(Thought.created_at)
    )
    thoughts = thoughts_result.scalars().all()

    if not body.title:
        if body.period_type == "week":
            title = f"{body.period_start.strftime('%m月%d日')} 周记"
        elif body.period_type == "month":
            title = f"{body.period_start.strftime('%Y年%m月')} 月记"
        else:
            title = f"{body.period_start} ~ {body.period_end} 回顾"
    else:
        title = body.title

    # 收集实际涉及的分类ID（从查询结果中获取）
    actual_category_ids = list(set([t.category_id for t in thoughts if t.category_id]))
    
    # 使用用户选择的分类ID（如果有），否则使用实际的分类ID
    saved_category_ids = body.category_ids if body.category_ids and len(body.category_ids) > 0 else actual_category_ids

    review = Review(
        id=str(uuid.uuid4()),
        user_id=user_id,
        period_type=body.period_type,
        period_start=body.period_start,
        period_end=body.period_end,
        title=title,
        thought_ids=[t.id for t in thoughts],
        thought_count=len(thoughts),
        category_ids=saved_category_ids,  # 保存用户选择的分类ID
        theme=body.theme,
        review_mode=body.review_mode,
        ai_content=body.ai_content,  # 保存AI生成的内容
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)

    return {
        **review_to_dict(review),
        "thoughts": [
            {"id": t.id, "content": t.content, "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S"), "tags": t.tags}
            for t in thoughts
        ],
    }


@router.get("/")
async def list_reviews(
    period_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    conditions = [Review.user_id == user_id]
    if period_type:
        conditions.append(Review.period_type == period_type)

    total_result = await db.execute(
        select(func.count()).select_from(Review).where(and_(*conditions))
    )
    total = total_result.scalar()

    result = await db.execute(
        select(Review)
        .where(and_(*conditions))
        .order_by(desc(Review.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    reviews = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [review_to_dict(r) for r in reviews],
    }


@router.get("/latest-week")
async def get_latest_week_review(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    thoughts_result = await db.execute(
        select(Thought).where(
            and_(
                Thought.user_id == user_id,
                Thought.is_deleted == False,
                Thought.created_at >= datetime.combine(week_start, time.min),
                Thought.created_at <= datetime.combine(week_end, time.max),
            )
        ).order_by(Thought.created_at)
    )
    thoughts = thoughts_result.scalars().all()

    return {
        "period_start": week_start,
        "period_end": week_end,
        "thought_count": len(thoughts),
        "thoughts": [
            {"id": t.id, "content": t.content, "created_at": t.created_at, "tags": t.tags}
            for t in thoughts
        ],
    }


@router.get("/{review_id}")
async def get_review(
    review_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Review).where(Review.id == review_id, Review.user_id == user_id)
    )
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="回顾不存在")

    # 根据保存的thought_ids查询想法
    thoughts_result = await db.execute(
        select(Thought).where(Thought.id.in_(review.thought_ids or []))
    )
    thoughts = thoughts_result.scalars().all()

    return {
        **review_to_dict(review),
        "thoughts": [
            {"id": t.id, "content": t.content, "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S"), "tags": t.tags}
            for t in thoughts
        ],
    }


@router.put("/{review_id}")
async def update_review(
    review_id: str,
    body: ReviewUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Review).where(Review.id == review_id, Review.user_id == user_id)
    )
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="回顾不存在")

    if body.ai_insights is not None:
        review.ai_insights = body.ai_insights
    if body.ai_summary is not None:
        review.ai_summary = body.ai_summary
    if body.ai_keywords is not None:
        review.ai_keywords = body.ai_keywords

    await db.commit()
    return review_to_dict(review)


@router.delete("/{review_id}")
async def delete_review(
    review_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Review).where(Review.id == review_id, Review.user_id == user_id)
    )
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="回顾不存在")

    await db.delete(review)
    await db.commit()
    return {"message": "删除成功"}
