from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.websocket_manager import manager

router = APIRouter()


@router.get("/online")
async def get_online_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(User).where(User.is_online == True))
    users = result.scalars().all()
    return [u.id for u in users if u.id != current_user.id]


@router.post("/set-online")
async def set_online(
    current_user: User = Depends(get_current_user)
):
    manager.disconnect(current_user.id)
    return {"status": "ok"}
