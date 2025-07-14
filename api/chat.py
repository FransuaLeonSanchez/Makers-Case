from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from database import get_session
from services.chat_service import ChatService
from services.inventory_service import InventoryService
from models.chat import ChatResponse, ChatSession
from config import settings

router = APIRouter(prefix="/api/chat", tags=["chat"])

chat_service = ChatService(use_mock=settings.use_mock_llm)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class SessionResponse(BaseModel):
    session_id: str
    message: str

@router.post("/start", response_model=SessionResponse)
async def start_chat_session():
    session_id = chat_service.create_session()
    return SessionResponse(
        session_id=session_id,
        message="¡Hola! Bienvenido a Makers Tech. ¿En qué puedo ayudarte hoy?"
    )

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    if not request.session_id:
        request.session_id = chat_service.create_session()
    
    inventory_service = InventoryService(session)
    
    try:
        response = await chat_service.process_message(
            session_id=request.session_id,
            message=request.message,
            inventory_service=inventory_service
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando mensaje: {str(e)}")

@router.get("/session/{session_id}")
async def get_chat_session(session_id: str):
    session = chat_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return {
        "session_id": session.session_id,
        "messages": [
            {
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in session.messages
            if msg.role.value != "system"
        ],
        "created_at": session.created_at.isoformat(),
        "last_activity": session.last_activity.isoformat()
    }

@router.delete("/session/{session_id}")
async def clear_chat_session(session_id: str):
    chat_service.clear_session(session_id)
    return {"message": "Sesión eliminada exitosamente"} 