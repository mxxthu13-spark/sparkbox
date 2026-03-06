from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from core.database import get_db
from core.security import get_current_user_id
from models.thought import Thought
from models.review import Review
from models.user import User
from services.ai import get_ai_service

router = APIRouter(prefix="/ai", tags=["AI 提炼"])


class RefineRequest(BaseModel):
    content: str
    mode: str = "polish"  # polish | expand | quote | copywrite


class SummarizeRequest(BaseModel):
    thought_ids: list[str]


class MonthlyReportRequest(BaseModel):
    review_id: str


class GenerateReviewRequest(BaseModel):
    start_date: str
    end_date: str
    category_ids: Optional[list[str]] = None
    style: str = "summary"  # summary | insight | soul


async def _get_user_ai_service(user_id: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    provider = user.ai_provider if user else "deepseek"
    return get_ai_service(provider)


@router.post("/refine")
async def refine_thought(
    body: RefineRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    if body.mode not in ("polish", "expand", "quote", "copywrite"):
        raise HTTPException(status_code=400, detail="不支持的处理模式")

    service = await _get_user_ai_service(user_id, db)
    result = await service.refine_thought(body.content, body.mode)
    return {"result": result, "mode": body.mode}


@router.post("/summarize")
async def summarize_thoughts(
    body: SummarizeRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    if not body.thought_ids:
        raise HTTPException(status_code=400, detail="请至少选择一条想法")
    if len(body.thought_ids) > 50:
        raise HTTPException(status_code=400, detail="一次最多处理 50 条想法")

    thoughts_result = await db.execute(
        select(Thought).where(
            Thought.id.in_(body.thought_ids),
            Thought.user_id == user_id,
            Thought.is_deleted == False,
        )
    )
    thoughts = thoughts_result.scalars().all()
    if not thoughts:
        raise HTTPException(status_code=404, detail="未找到对应的想法")

    service = await _get_user_ai_service(user_id, db)
    contents = [t.content for t in thoughts]
    result = await service.summarize_thoughts(contents)

    for thought in thoughts:
        if result.get("quote"):
            thought.ai_quote = result["quote"]
    await db.commit()

    return result


@router.post("/monthly-report")
async def generate_monthly_report(
    body: MonthlyReportRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    review_result = await db.execute(
        select(Review).where(Review.id == body.review_id, Review.user_id == user_id)
    )
    review = review_result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="回顾不存在")

    thoughts_result = await db.execute(
        select(Thought).where(
            Thought.id.in_(review.thought_ids or []),
            Thought.is_deleted == False,
        )
    )
    thoughts = thoughts_result.scalars().all()
    if not thoughts:
        raise HTTPException(status_code=400, detail="该回顾没有关联的想法")

    service = await _get_user_ai_service(user_id, db)
    month_str = review.period_start.strftime("%Y年%m月")
    thought_dicts = [
        {
            "content": t.content,
            "created_at": t.created_at.strftime("%m/%d"),
            "category": t.category_id or "",
        }
        for t in thoughts
    ]
    result = await service.generate_monthly_report(thought_dicts, month_str)

    review.ai_insights = result.get("growth", "")
    review.ai_summary = result.get("summary", "")
    review.ai_keywords = result.get("keywords", [])
    await db.commit()

    return result


@router.post("/generate-review")
async def generate_review(
    body: GenerateReviewRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime, timedelta
    from models.thought import CHINA_TZ
    
    # 解析日期，结束日期需要加一天以包含当天
    try:
        # 创建带时区的 datetime 对象
        start = datetime.strptime(body.start_date, "%Y-%m-%d")
        end = datetime.strptime(body.end_date, "%Y-%m-%d") + timedelta(days=1)
        
        # 由于数据库存储的是 naive datetime，我们也用 naive datetime 查询
        # 不需要添加时区信息
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误")
    
    # 查询想法
    query = select(Thought).where(
        Thought.user_id == user_id,
        Thought.is_deleted == False,
        Thought.created_at >= start,
        Thought.created_at < end,
    )
    
    if body.category_ids:
        query = query.where(Thought.category_id.in_(body.category_ids))
    
    thoughts_result = await db.execute(query)
    thoughts = thoughts_result.scalars().all()
    
    if not thoughts:
        # 返回友好提示而不是抛出异常
        return {
            "summary": "该时间段没有想法记录",
            "insight": "该时间段没有想法记录",
            "soul": "该时间段没有想法记录",
            "theme": "",
            "thought_count": 0,
            "days": 0,
            "categories": 0,
        }
    
    # 调用 AI 服务生成回顾
    service = await _get_user_ai_service(user_id, db)
    thought_contents = [t.content for t in thoughts]
    
    try:
        result = await service.generate_three_mode_review(thought_contents, body.style)
    except Exception as e:
        # AI 服务调用失败时返回错误信息
        return {
            "summary": f"AI 服务暂时不可用: {str(e)}",
            "insight": f"AI 服务暂时不可用: {str(e)}",
            "soul": f"AI 服务暂时不可用: {str(e)}",
            "theme": "",
            "thought_count": len(thoughts),
            "days": len(set(t.created_at.date() for t in thoughts)),
            "categories": len(set(t.category_id for t in thoughts if t.category_id)),
            "thoughts": [],
        }
    
    # 添加统计信息和原始想法记录
    result["thought_count"] = len(thoughts)
    result["days"] = len(set(t.created_at.date() for t in thoughts))
    result["categories"] = len(set(t.category_id for t in thoughts if t.category_id))
    result["thoughts"] = [
        {
            "id": t.id,
            "content": t.content,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "category_id": t.category_id,
        }
        for t in thoughts
    ]
    
    return result
