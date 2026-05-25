from fastapi import WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager
from app.core.security import decode_token
from app.core.database import AsyncSession, get_db
from app.models.user import User
from sqlalchemy import select


async def websocket_endpoint(websocket: WebSocket, token: str):
    await websocket.accept()
    
    # Decode token to get user_id
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=4001)
        return
    
    user_id = payload.get("sub")
    
    # Connect user
    await manager.connect(user_id, websocket)
    
    # Update online status
    async with AsyncSession(get_db) as db:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.is_online = True
    
    # Notify contacts
    await manager.broadcast({
        "type": "user_online",
        "user_id": user_id
    })
    
    try:
        while True:
            data = await websocket.receive_json()
            await handle_message(user_id, data)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        # Update offline status
        async with AsyncSession(get_db) as db:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                user.is_online = False
                user.last_seen = datetime.utcnow()
        
        await manager.broadcast({
            "type": "user_offline",
            "user_id": user_id
        })


async def handle_message(user_id: str, data: dict):
    msg_type = data.get("type")
    
    if msg_type == "send_message":
        await manager.broadcast_to_chat(
            data["chat_id"],
            {
                "type": "new_message",
                "message": data["message"]
            },
            exclude_user_id=user_id
        )
    
    elif msg_type == "typing":
        manager.set_typing(user_id, data["chat_id"])
        typing_users = manager.get_typing_users(data["chat_id"])
        await manager.broadcast_to_chat(data["chat_id"], {
            "type": "user_typing",
            "user_id": user_id,
            "chat_id": data["chat_id"]
        }, exclude_user_id=user_id)
    
    elif msg_type == "stop_typing":
        manager.remove_typing(user_id, data["chat_id"])
        await manager.broadcast_to_chat(data["chat_id"], {
            "type": "user_stop_typing",
            "user_id": user_id,
            "chat_id": data["chat_id"]
        }, exclude_user_id=user_id)
    
    elif msg_type == "mark_read":
        await manager.broadcast_to_chat(data["chat_id"], {
            "type": "messages_read",
            "chat_id": data["chat_id"],
            "message_ids": data["message_ids"],
            "read_by": user_id
        })
