from typing import Dict, Set
from fastapi import WebSocket
import json
import asyncio
from app.core.config import settings


class ConnectionManager:
    def __init__(self):
        # user_id -> websocket
        self.active_connections: Dict[str, WebSocket] = {}
        # user_id -> set of chat_ids being typed in
        self.typing: Dict[str, Set[str]] = {}
        # chat_id -> set of user_ids
        self.chat_rooms: Dict[str, Set[str]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        self.typing.pop(user_id, None)

    async def send_personal(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def broadcast_to_chat(self, chat_id: str, message: dict, exclude_user_id: str = None):
        if chat_id in self.chat_rooms:
            for user_id in self.chat_rooms[chat_id]:
                if user_id != exclude_user_id:
                    await self.send_personal(user_id, message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

    def set_typing(self, user_id: str, chat_id: str):
        if user_id not in self.typing:
            self.typing[user_id] = set()
        self.typing[user_id].add(chat_id)

    def remove_typing(self, user_id: str, chat_id: str):
        if user_id in self.typing:
            self.typing[user_id].discard(chat_id)

    def get_typing_users(self, chat_id: str) -> Set[str]:
        typing_users = set()
        for user_id, chats in self.typing.items():
            if chat_id in chats:
                typing_users.add(user_id)
        return typing_users

    def join_chat(self, chat_id: str, user_id: str):
        if chat_id not in self.chat_rooms:
            self.chat_rooms[chat_id] = set()
        self.chat_rooms[chat_id].add(user_id)

    def leave_chat(self, chat_id: str, user_id: str):
        if chat_id in self.chat_rooms:
            self.chat_rooms[chat_id].discard(user_id)


manager = ConnectionManager()
