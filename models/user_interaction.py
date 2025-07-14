from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.product import Base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    category_viewed = Column(String, nullable=True)
    search_query = Column(Text, nullable=True)
    interaction_type = Column(String)  # "view", "search", "chat_mention", "recommendation_click"
    timestamp = Column(DateTime, default=datetime.now)
    
    product = relationship("Product", lazy="joined")

class GlobalUserPreference(Base):
    __tablename__ = "global_user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    preferred_categories = Column(Text)  # JSON string
    preferred_brands = Column(Text)  # JSON string
    price_range_min = Column(Float, default=0)
    price_range_max = Column(Float, default=50000)
    interaction_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.now)

class InteractionRequest(BaseModel):
    product_id: Optional[int] = None
    category_viewed: Optional[str] = None
    search_query: Optional[str] = None
    interaction_type: str

class PreferenceUpdate(BaseModel):
    categories: List[str] = []
    brands: List[str] = []
    price_min: float = 0
    price_max: float = 50000

# Mantener UserPreference por compatibilidad temporal
UserPreference = GlobalUserPreference 