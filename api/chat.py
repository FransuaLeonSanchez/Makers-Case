from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List
from database import get_session
from services.chat_service import ChatService
from services.inventory_service import InventoryService
from services.recommendation_service import RecommendationService
from models.chat import ChatResponse, ChatHistory, ChatMessage
from config import settings
from sqlalchemy import select, delete, func
from datetime import datetime
import json

router = APIRouter(prefix="/api/chat", tags=["chat"])

chat_service = ChatService(use_mock=settings.use_mock_llm)

class ChatRequest(BaseModel):
    message: str

class MessageHistoryResponse(BaseModel):
    messages: List[dict]
    total: int

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    inventory_service = InventoryService(session)
    recommendation_service = RecommendationService(session)
    
    try:
        response = await chat_service.process_message(
            message=request.message,
            inventory_service=inventory_service,
            recommendation_service=recommendation_service,
            db_session=session
        )
        # Asegurar que los cambios se guarden
        await session.commit()
        return response
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=MessageHistoryResponse)
async def get_chat_history(
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene el historial de chat global"""
    try:
        # Obtener mensajes del historial
        result = await session.execute(
            select(ChatHistory)
            .order_by(ChatHistory.timestamp.desc())
            .limit(limit)
            .offset(offset)
        )
        messages = result.scalars().all()
        
        # Contar total de mensajes
        count_result = await session.execute(
            select(func.count(ChatHistory.id))
        )
        total = count_result.scalar()
        
        # Formatear mensajes
        formatted_messages = [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "products_mentioned": json.loads(msg.products_mentioned) if msg.products_mentioned else []
            }
            for msg in reversed(messages)  # Revertir para orden cronológico
        ]
        
        return MessageHistoryResponse(
            messages=formatted_messages,
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clear")
async def clear_chat_history(
    session: AsyncSession = Depends(get_session)
):
    """Limpia el historial de chat (para empezar una nueva conversación)"""
    try:
        await session.execute(
            delete(ChatHistory)
        )
        await session.commit()
        return {"message": "Historial de chat limpiado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 