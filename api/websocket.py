from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import json
import logging
from database import get_session
from services.chat_service import ChatService
from services.inventory_service import InventoryService
from config import settings

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"Cliente conectado: {session_id}")
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"Cliente desconectado: {session_id}")
    
    async def send_message(self, message: str, session_id: str):
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            await websocket.send_text(message)

manager = ConnectionManager()
chat_service = ChatService(use_mock=settings.use_mock_llm)

async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    
    if not chat_service.get_session(session_id):
        chat_service.create_session(session_id)
        await manager.send_message(
            json.dumps({
                "type": "welcome",
                "message": "¡Hola! Bienvenido a Makers Tech. ¿En qué puedo ayudarte hoy?",
                "session_id": session_id
            }),
            session_id
        )
    
    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                
                if not user_message:
                    await manager.send_message(
                        json.dumps({
                            "type": "error",
                            "message": "Mensaje vacío"
                        }),
                        session_id
                    )
                    continue
                
                async for session in get_session():
                    inventory_service = InventoryService(session)
                    
                    response = await chat_service.process_message(
                        session_id=session_id,
                        message=user_message,
                        inventory_service=inventory_service
                    )
                    
                    await manager.send_message(
                        json.dumps({
                            "type": "response",
                            "message": response.message,
                            "timestamp": response.timestamp.isoformat(),
                            "products_mentioned": response.products_mentioned
                        }),
                        session_id
                    )
                    break
                    
            except json.JSONDecodeError:
                await manager.send_message(
                    json.dumps({
                        "type": "error",
                        "message": "Formato de mensaje inválido"
                    }),
                    session_id
                )
            except Exception as e:
                logger.error(f"Error procesando mensaje: {str(e)}")
                await manager.send_message(
                    json.dumps({
                        "type": "error",
                        "message": "Error interno del servidor"
                    }),
                    session_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"Error en WebSocket: {str(e)}")
        manager.disconnect(session_id) 