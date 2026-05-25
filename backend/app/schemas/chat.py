from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatBase(BaseModel):
    name: Optional[str] = None
    chat_type: str = "private"
    avatar: Optional[str] = None


class ChatCreate(ChatBase):
    member_ids: List[str]


class ChatResponse(ChatBase):
    id: str
    members: List[dict]
    last_message: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True
