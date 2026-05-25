from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageBase(BaseModel):
    content: str
    message_type: str = "text"
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    reply_to_id: Optional[str] = None


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: str
    chat_id: str
    sender_id: str
    sender_username: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
