from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from core.database import get_db
from core.security import hash_password, verify_password, create_access_token, get_current_user_id
from models.user import User
from models.category import Category, DEFAULT_CATEGORIES
import uuid

router = APIRouter(prefix="/auth", tags=["认证"])


class PhoneLoginRequest(BaseModel):
    phone: str
    password: str


class RegisterRequest(BaseModel):
    phone: str
    password: str
    nickname: Optional[str] = "闪念用户"


class WechatLoginRequest(BaseModel):
    code: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    nickname: str
    avatar_url: Optional[str]


async def _create_default_categories(user_id: str, db: AsyncSession):
    for i, cat in enumerate(DEFAULT_CATEGORIES):
        category = Category(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=cat["name"],
            icon=cat["icon"],
            color=cat["color"],
            sort_order=i,
            is_default=True,
        )
        db.add(category)
    await db.commit()


@router.post("/register", response_model=TokenResponse)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.phone == body.phone))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该手机号已注册")

    user = User(
        id=str(uuid.uuid4()),
        phone=body.phone,
        nickname=body.nickname or "闪念用户",
        password_hash=hash_password(body.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await _create_default_categories(user.id, db)

    token = create_access_token({"sub": user.id})
    return TokenResponse(
        access_token=token, user_id=user.id, nickname=user.nickname, avatar_url=user.avatar_url
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: PhoneLoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.phone == body.phone))
    user = result.scalar_one_or_none()
    if not user or not user.password_hash or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="手机号或密码错误")

    token = create_access_token({"sub": user.id})
    return TokenResponse(
        access_token=token, user_id=user.id, nickname=user.nickname, avatar_url=user.avatar_url
    )


@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {
        "user_id": user.id,
        "phone": user.phone,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "ai_provider": user.ai_provider,
        "created_at": user.created_at,
    }


class UpdateProfileRequest(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    ai_provider: Optional[str] = None


@router.put("/me")
async def update_profile(
    body: UpdateProfileRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if body.nickname is not None:
        user.nickname = body.nickname
    if body.avatar_url is not None:
        user.avatar_url = body.avatar_url
    if body.ai_provider is not None:
        if body.ai_provider not in ("deepseek", "qwen", "ernie"):
            raise HTTPException(status_code=400, detail="不支持的 AI 提供商")
        user.ai_provider = body.ai_provider

    await db.commit()
    return {"message": "更新成功"}
