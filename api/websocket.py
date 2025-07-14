from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import json
import logging
from database import get_session
from services.chat_service import ChatService
from services.inventory_service import InventoryService
from services.recommendation_service import RecommendationService
from config import settings

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Cliente conectado. Total conexiones: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Cliente desconectado. Total conexiones: {len(self.active_connections)}")
    
    async def send_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")

manager = ConnectionManager()
chat_service = ChatService(use_mock=settings.use_mock_llm)

async def websocket_endpoint(websocket: WebSocket, db_session: AsyncSession = Depends(get_session)):
    await manager.connect(websocket)
    
    # Enviar mensaje de bienvenida
    await manager.send_message(
        json.dumps({
            "type": "welcome",
            "message": "¡Hola! Bienvenido a Makers Tech. ¿En qué puedo ayudarte hoy?"
        }),
        websocket
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
                        websocket
                    )
                    continue
                
                # Mostrar indicador de escritura
                await manager.send_message(
                    json.dumps({
                        "type": "typing"
                    }),
                    websocket
                )
                
                inventory_service = InventoryService(db_session)
                recommendation_service = RecommendationService(db_session)
                
                response = await chat_service.process_message(
                    message=user_message,
                    inventory_service=inventory_service,
                    recommendation_service=recommendation_service,
                    db_session=db_session
                )
                
                await manager.send_message(
                    json.dumps({
                        "type": "response",
                        "message": response.message,
                        "timestamp": response.timestamp.isoformat(),
                        "products_mentioned": response.products_mentioned
                    }),
                    websocket
                )
                    
            except json.JSONDecodeError:
                await manager.send_message(
                    json.dumps({
                        "type": "error",
                        "message": "Formato de mensaje inválido"
                    }),
                    websocket
                )
            except Exception as e:
                logger.error(f"Error procesando mensaje: {str(e)}")
                await manager.send_message(
                    json.dumps({
                        "type": "error",
                        "message": "Error interno del servidor"
                    }),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Error en WebSocket: {str(e)}")
        manager.disconnect(websocket) 