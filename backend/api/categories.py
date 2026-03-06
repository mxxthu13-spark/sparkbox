from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from core.database import get_db
from core.security import get_current_user_id
from models.category import Category
import uuid

router = APIRouter(prefix="/categories", tags=["分类"])


class CategoryCreate(BaseModel):
    name: str
    icon: str = "💡"
    color: str = "#6366f1"
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    sort_order: Optional[int] = None


def category_to_dict(cat: Category) -> dict:
    return {
        "id": cat.id,
        "name": cat.name,
        "icon": cat.icon,
        "color": cat.color,
        "sort_order": cat.sort_order,
        "is_default": cat.is_default,
        "created_at": cat.created_at,
    }


@router.get("/")
async def list_categories(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Category)
        .where(Category.user_id == user_id)
        .order_by(Category.sort_order, Category.created_at)
    )
    categories = result.scalars().all()
    return [category_to_dict(c) for c in categories]


@router.post("/")
async def create_category(
    body: CategoryCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    category = Category(
        id=str(uuid.uuid4()),
        user_id=user_id,
        name=body.name,
        icon=body.icon,
        color=body.color,
        sort_order=body.sort_order,
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category_to_dict(category)


@router.put("/{category_id}")
async def update_category(
    category_id: str,
    body: CategoryUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Category).where(Category.id == category_id, Category.user_id == user_id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    if body.name is not None:
        category.name = body.name
    if body.icon is not None:
        category.icon = body.icon
    if body.color is not None:
        category.color = body.color
    if body.sort_order is not None:
        category.sort_order = body.sort_order

    await db.commit()
    return category_to_dict(category)


@router.delete("/{category_id}")
async def delete_category(
    category_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Category).where(Category.id == category_id, Category.user_id == user_id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    if category.is_default:
        raise HTTPException(status_code=400, detail="默认分类不可删除")

    await db.delete(category)
    await db.commit()
    return {"message": "删除成功"}
