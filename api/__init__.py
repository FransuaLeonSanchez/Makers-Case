from .products import router as products_router
from .chat import router as chat_router
from .recommendations import router as recommendations_router
from .websocket import websocket_endpoint

__all__ = ["products_router", "chat_router", "recommendations_router", "websocket_endpoint"] 