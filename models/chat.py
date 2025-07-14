from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Text
from models.product import Base

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)
    products_mentioned = Column(Text)  # JSON string
    
class ChatResponse(BaseModel):
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    products_mentioned: Optional[List[int]] = None
    
class MultiChatResponse(BaseModel):
    messages: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)
    products_mentioned: Optional[List[int]] = None
    
class ChatRequest(BaseModel):
    message: str 