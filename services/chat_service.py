from typing import List, Dict, Optional, Any
from models.chat import ChatMessage, ChatSession, MessageRole, ChatResponse
from services.inventory_service import InventoryService
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema.output import ChatResult, ChatGeneration
from langchain.schema.messages import BaseMessageChunk
import json
import re
import uuid
from datetime import datetime

class MockChatModel(BaseChatModel):
    """Modelo de chat simulado para desarrollo sin necesidad de API key"""
    
    @property
    def _llm_type(self) -> str:
        return "mock"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        last_message = messages[-1].content if messages else ""
        response = self._generate_mock_response(last_message)
        message = AIMessage(content=response)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])
    
    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        return self._generate(messages, stop, run_manager, **kwargs)
    
    def _generate_mock_response(self, user_input: str) -> str:
        user_input_lower = user_input.lower()
        
        if "hola" in user_input_lower or "buenos" in user_input_lower:
            return "¡Hola! Bienvenido a Makers Tech. Soy tu asistente virtual y estoy aquí para ayudarte con información sobre nuestros productos. ¿En qué puedo ayudarte hoy?"
        
        elif "computadora" in user_input_lower or "computador" in user_input_lower or "desktop" in user_input_lower:
            return "En este momento tenemos 1 computadora de escritorio disponible: la Dell OptiPlex 3000. Es una computadora compacta y potente ideal para oficina, con procesador Intel Core i5-12500, 8GB de RAM y 256GB SSD. Su precio es de $799.99. ¿Te gustaría conocer más detalles sobre este equipo?"
        
        elif "laptop" in user_input_lower or "portátil" in user_input_lower:
            return "Actualmente tenemos 3 modelos de laptops disponibles:\n\n1. **HP Pavilion 15** - $899.99 (5 unidades)\n2. **HP ProBook 450** - $1,299.99 (3 unidades)\n3. **MacBook Air M2** - $1,499.99 (1 unidad)\n\n¿Cuál te gustaría conocer con más detalle?"
        
        elif "dell" in user_input_lower:
            return "La Dell OptiPlex 3000 es una excelente computadora de escritorio. Aquí están sus características principales:\n\n- **Procesador:** Intel Core i5-12500\n- **Memoria RAM:** 8GB DDR4\n- **Almacenamiento:** 256GB SSD\n- **Sistema Operativo:** Windows 11 Pro\n- **Conectividad:** USB 3.0, HDMI, DisplayPort\n- **Precio:** $799.99\n- **Stock:** 2 unidades disponibles\n\nEs perfecta para trabajo de oficina y tareas profesionales. ¿Te interesa adquirirla?"
        
        elif "precio" in user_input_lower or "costo" in user_input_lower or "cuánto" in user_input_lower:
            return "Por supuesto, aquí están algunos de nuestros precios destacados:\n\n- Laptops desde $899.99\n- Tablets desde $699.99\n- Celulares desde $1,199.99\n- Monitores desde $599.99\n- Accesorios desde $89.99\n\n¿Qué categoría de productos te interesa más?"
        
        elif "tablet" in user_input_lower:
            return "Tenemos 2 excelentes tablets disponibles:\n\n1. **iPad Pro 12.9** - $1,099.99 (4 unidades)\n   - Chip Apple M2, pantalla Liquid Retina XDR\n\n2. **Samsung Galaxy Tab S8** - $699.99 (6 unidades)\n   - Snapdragon 8 Gen 1, incluye S Pen\n\n¿Cuál prefieres conocer en detalle?"
        
        elif "teléfono" in user_input_lower or "celular" in user_input_lower or "móvil" in user_input_lower:
            return "En celulares tenemos dos opciones premium:\n\n1. **iPhone 14 Pro** - $1,299.99 (7 unidades)\n   - Chip A16 Bionic, cámara de 48MP\n\n2. **Samsung Galaxy S23 Ultra** - $1,199.99 (5 unidades)\n   - Snapdragon 8 Gen 2, S Pen integrado\n\n¿Te gustaría más información sobre alguno?"
        
        elif "stock" in user_input_lower or "inventario" in user_input_lower or "disponible" in user_input_lower:
            return "Nuestro inventario actual incluye:\n\n- **Computadoras:** 1 modelo (2 unidades)\n- **Laptops:** 3 modelos (9 unidades)\n- **Tablets:** 2 modelos (10 unidades)\n- **Celulares:** 2 modelos (12 unidades)\n- **Monitores:** 1 modelo (8 unidades)\n- **Accesorios:** Varios modelos disponibles\n\n¿Qué categoría te interesa explorar?"
        
        else:
            return "Disculpa, no estoy seguro de entender tu consulta. Puedo ayudarte con información sobre:\n\n- Computadoras y laptops\n- Tablets y celulares\n- Monitores y periféricos\n- Precios y disponibilidad\n- Características técnicas\n\n¿Qué te gustaría saber?"

class ChatService:
    def __init__(self, use_mock: bool = True):
        self.sessions: Dict[str, ChatSession] = {}
        self.use_mock = use_mock
        
        if use_mock:
            self.llm = MockChatModel()
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        if not session_id:
            session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = ChatSession(
            session_id=session_id,
            messages=[
                ChatMessage(
                    role=MessageRole.SYSTEM,
                    content="""Eres un asistente virtual de Makers Tech, una tienda de tecnología.
                    Tu trabajo es ayudar a los clientes con información sobre productos, precios y disponibilidad.
                    Siempre sé amable, profesional y responde en español.
                    Cuando menciones productos, incluye precio y stock disponible."""
                )
            ]
        )
        return session_id
    
    async def process_message(
        self, 
        session_id: str, 
        message: str,
        inventory_service: Optional[InventoryService] = None
    ) -> ChatResponse:
        if session_id not in self.sessions:
            session_id = self.create_session(session_id)
        
        session = self.sessions[session_id]
        
        session.messages.append(
            ChatMessage(role=MessageRole.USER, content=message)
        )
        
        context = ""
        products_mentioned = []
        
        if inventory_service:
            context = await self._build_context(message, inventory_service)
            products_mentioned = await self._extract_product_ids(message, inventory_service)
        
        messages = self._prepare_langchain_messages(session, context)
        
        response = await self.llm.agenerate([messages])
        response_text = response.generations[0][0].text
        
        session.messages.append(
            ChatMessage(role=MessageRole.ASSISTANT, content=response_text)
        )
        session.last_activity = datetime.now()
        
        return ChatResponse(
            message=response_text,
            session_id=session_id,
            products_mentioned=products_mentioned if products_mentioned else None
        )
    
    def _prepare_langchain_messages(self, session: ChatSession, context: str) -> List[BaseMessage]:
        messages = []
        
        for msg in session.messages:
            if msg.role == MessageRole.SYSTEM:
                system_content = msg.content
                if context:
                    system_content += f"\n\nContexto actual del inventario:\n{context}"
                messages.append(SystemMessage(content=system_content))
            elif msg.role == MessageRole.USER:
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == MessageRole.ASSISTANT:
                messages.append(AIMessage(content=msg.content))
        
        return messages
    
    async def _build_context(self, message: str, inventory_service: InventoryService) -> str:
        context_parts = []
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["inventario", "stock", "disponible", "cuántos", "cuántas"]):
            summary = await inventory_service.get_inventory_summary()
            context_parts.append(f"Resumen de inventario: {json.dumps(summary, ensure_ascii=False)}")
        
        search_results = await inventory_service.search_products(message)
        if search_results:
            products_info = []
            for product in search_results[:5]:
                products_info.append(
                    f"- {product.name} ({product.brand}): ${product.price}, Stock: {product.stock}"
                )
            context_parts.append("Productos relevantes encontrados:\n" + "\n".join(products_info))
        
        return "\n\n".join(context_parts)
    
    async def _extract_product_ids(self, message: str, inventory_service: InventoryService) -> List[int]:
        search_results = await inventory_service.search_products(message)
        return [product.id for product in search_results[:3]]
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        return self.sessions.get(session_id)
    
    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id] 