from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.chat import Chat, ChatMember
from app.models.message import Message
from app.schemas.chat import ChatCreate, ChatResponse
from app.core.websocket_manager import manager
from uuid import uuid4
from typing import List

router = APIRouter()


@router.get("/")
async def get_chats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[ChatResponse]:
    result = await db.execute(
        select(ChatMember)
        .where(ChatMember.user_id == current_user.id, ChatMember.is_active == True)
        .join(Chat)
        .order_by(Chat.updated_at.desc())
    )
    members = result.scalars().all()

    chats = []
    for cm in members:
        chat = cm.chat
        # Get last message
        last_msg = await db.execute(
            select(Message).where(Message.chat_id == chat.id).order_by(Message.created_at.desc()).limit(1)
        )
        lm = last_msg.scalar_one_or_none()
        chats.append(ChatResponse(
            id=chat.id,
            name=chat.name,
            chat_type=chat.chat_type,
            avatar=chat.avatar,
            members=[{"id": m.user_id, "role": m.role} for m in chat.members],
            last_message={"id": lm.id, "content": lm.content, "created_at": lm.created_at.isoformat()} if lm else None,
            created_at=chat.created_at
        ))
    return chats


@router.post("/")
async def create_chat(
    create: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    chat_id = str(uuid4())
    chat = Chat(id=chat_id, name=create.name, chat_type=create.chat_type)
    db.add(chat)
    await db.flush()

    for member_id in [current_user.id] + create.member_ids:
        cm = ChatMember(id=str(uuid4()), chat_id=chat_id, user_id=member_id)
        db.add(cm)

    await db.commit()
    await db.refresh(chat)

    # Join WebSocket room
    manager.join_chat(chat_id, current_user.id)

    return ChatResponse(
        id=chat.id,
        name=chat.name,
        chat_type=chat.chat_type,
        members=[{"id": m.user_id, "role": m.role} for m in chat.members],
        created_at=chat.created_at
    )
