from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.db.models import MessageRole

class MessageBase(BaseModel):
    role: MessageRole
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True

class ConversationWithMessages(Conversation):
    messages: List[Message] = Field(default_factory=list) 