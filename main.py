from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from config import settings
from database import init_db, get_session
from api import products_router, chat_router, websocket_endpoint
from services.inventory_service import InventoryService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación...")
    await init_db()
    
    async for session in get_session():
        inventory_service = InventoryService(session)
        await inventory_service.init_synthetic_data()
        logger.info("Datos sintéticos cargados")
        break
    
    yield
    
    logger.info("Cerrando aplicación...")

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API del ChatBot de Makers Tech para consultas de inventario",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a Makers Tech ChatBot API",
        "version": "1.0.0",
        "endpoints": {
            "products": "/api/products",
            "chat": "/api/chat",
            "websocket": "/ws/{session_id}",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "makers-tech-chatbot"}

@app.websocket("/ws/{session_id}")
async def websocket_route(websocket: WebSocket, session_id: str):
    await websocket_endpoint(websocket, session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 