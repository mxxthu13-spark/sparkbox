from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, and_
from pydantic import BaseModel
from typing import Optional
from core.database import get_db
from core.security import get_current_user_id
from models.card import Card
import uuid

router = APIRouter(prefix="/cards", tags=["卡片"])

TEMPLATES = [
    {"id": "minimal", "name": "极简白", "preview_color": "#ffffff", "text_color": "#1a1a1a"},
    {"id": "night", "name": "深夜黑", "preview_color": "#1a1a2e", "text_color": "#e8e8ff"},
    {"id": "forest", "name": "林间绿", "preview_color": "#1a3a2a", "text_color": "#c8f0d8"},
    {"id": "warm", "name": "暖橙", "preview_color": "#fff7ed", "text_color": "#7c2d12"},
    {"id": "note", "name": "手账风", "preview_color": "#fefce8", "text_color": "#713f12"},
]


class CardCreate(BaseModel):
    content: str
    template_id: str = "minimal"
    card_config: dict = {}
    thought_id: Optional[str] = None
    review_id: Optional[str] = None


def card_to_dict(c: Card) -> dict:
    return {
        "id": c.id,
        "content": c.content,
        "template_id": c.template_id,
        "card_config": c.card_config or {},
        "image_url": c.image_url,
        "thought_id": c.thought_id,
        "review_id": c.review_id,
        "created_at": c.created_at,
    }


@router.get("/templates")
async def list_templates():
    return TEMPLATES


@router.post("/")
async def create_card(
    body: CardCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    if body.template_id not in [t["id"] for t in TEMPLATES]:
        raise HTTPException(status_code=400, detail="不支持的模板")

    card = Card(
        id=str(uuid.uuid4()),
        user_id=user_id,
        content=body.content,
        template_id=body.template_id,
        card_config=body.card_config,
        thought_id=body.thought_id,
        review_id=body.review_id,
    )
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card_to_dict(card)


@router.get("/")
async def list_cards(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    total_result = await db.execute(
        select(func.count()).select_from(Card).where(Card.user_id == user_id)
    )
    total = total_result.scalar()

    result = await db.execute(
        select(Card)
        .where(Card.user_id == user_id)
        .order_by(desc(Card.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    cards = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [card_to_dict(c) for c in cards],
    }


@router.delete("/{card_id}")
async def delete_card(
    card_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Card).where(Card.id == card_id, Card.user_id == user_id)
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")

    await db.delete(card)
    await db.commit()
    return {"message": "删除成功"}
