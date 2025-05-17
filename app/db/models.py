from datetime import datetime
import enum
from app.db.base import db

class MessageRole(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 대화와 메시지 간의 관계 설정
    messages = db.relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'messages': [message.to_dict() for message in self.messages]
        }

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, index=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id", ondelete="CASCADE"))
    role = db.Column(db.Enum(MessageRole))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 메시지와 대화 간의 관계 설정
    conversation = db.relationship("Conversation", back_populates="messages")

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role.value,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        } 