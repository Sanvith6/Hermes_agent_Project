from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.chat import ChatMember
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse
from app.core.websocket_manager import manager
from uuid import uuid4
from typing import List

router = APIRouter()


@router.get("/{chat_id}/messages")
async def get_messages(
    chat_id: str,
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[MessageResponse]:
    # Verify user is member
    result = await db.execute(
        select(ChatMember).where(ChatMember.chat_id == chat_id, ChatMember.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a member of this chat")

    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .offset(offset).limit(limit)
    )
    messages = result.scalars().all()

    return [
        MessageResponse(
            id=m.id, chat_id=m.chat_id, sender_id=m.sender_id,
            content=m.content, message_type=m.message_type,
            file_url=m.file_url, file_name=m.file_name,
            status=m.status, created_at=m.created_at
        ) for m in reversed(messages)
    ]


@router.post("/{chat_id}/messages")
async def send_message(
    chat_id: str,
    create: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MessageResponse:
    # Verify user is member
    result = await db.execute(
        select(ChatMember).where(ChatMember.chat_id == chat_id, ChatMember.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Not a member of this chat")

    message = Message(
        id=str(uuid4()),
        chat_id=chat_id,
        sender_id=current_user.id,
        content=create.content,
        message_type=create.message_type,
        file_url=create.file_url,
        file_name=create.file_name
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    # Broadcast via WebSocket
    await manager.broadcast_to_chat(chat_id, {
        "type": "new_message",
        "message": {
            "id": message.id,
            "chat_id": message.chat_id,
            "sender_id": message.sender_id,
            "content": message.content,
            "message_type": message.message_type,
            "status": "sent",
            "created_at": message.created_at.isoformat()
        }
    }, exclude_user_id=current_user.id)

    return MessageResponse(
        id=message.id, chat_id=message.chat_id, sender_id=message.sender_id,
        content=message.content, message_type=message.message_type,
        file_url=message.file_url, file_name=message.file_name,
        status=message.status, created_at=message.created_at
    )
