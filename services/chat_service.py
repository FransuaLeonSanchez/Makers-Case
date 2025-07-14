from typing import List, Dict, Optional, Any
from models.chat import ChatMessage, MessageRole, ChatResponse, ChatHistory
from models.product import ProductCategory
from services.inventory_service import InventoryService
from services.recommendation_service import RecommendationService
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
import re
import os
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
        **kwargs: Any,
    ) -> ChatResult:
        return self._generate(messages, stop, **kwargs)
    
    def _generate_mock_response(self, user_input: str) -> str:
        user_input_lower = user_input.lower()
        
        if "hola" in user_input_lower or "buenos" in user_input_lower:
            return "¡Hola! Bienvenido a Makers Tech. Soy tu asistente virtual y estoy aquí para ayudarte con información sobre nuestros productos. ¿En qué puedo ayudarte hoy?"
        
        elif "computadora" in user_input_lower or "computador" in user_input_lower or "desktop" in user_input_lower:
            return """¡Claro! Te muestro las computadoras que tenemos disponibles:

Tenemos la **Dell OptiPlex 3000**, una excelente computadora de escritorio compacta y potente para oficina.
**Precio**: $799.99 - **Stock**: 2 unidades

También está disponible el **iMac 24 M3** de Apple, un all-in-one con pantalla Retina 4.5K.
**Precio**: $1599.99 - **Stock**: 3 unidades

Y el **HP Elite Tower 800 G9**, una workstation empresarial de alto rendimiento.
**Precio**: $1099.99 - **Stock**: 4 unidades

¿Te gustaría conocer más detalles sobre alguna de estas opciones?"""
        
        elif "laptop" in user_input_lower or "portátil" in user_input_lower:
            return """Por supuesto! Estas son nuestras laptops disponibles:

La **HP Pavilion 15** con procesador AMD Ryzen 5, ideal para trabajo y entretenimiento.
**Precio**: $899.99 - **Stock**: 5 unidades

También tenemos el **Lenovo ThinkPad X1 Carbon**, ultrabook empresarial premium.
**Precio**: $1799.99 - **Stock**: 4 unidades

¿Necesitas algo específico como gaming, trabajo profesional o uso general?"""
        
        elif "teléfono" in user_input_lower or "celular" in user_input_lower or "smartphone" in user_input_lower:
            return """¡Excelente! Te muestro nuestros smartphones disponibles:

El **iPhone 14 Pro** de Apple con Dynamic Island y cámara de 48MP.
**Precio**: $1299.99 - **Stock**: 7 unidades

El **Samsung Galaxy S23 Ultra** con S Pen integrado y cámara de 200MP.
**Precio**: $1199.99 - **Stock**: 5 unidades

También tenemos opciones más accesibles como el **Xiaomi Redmi Note 12 Pro**.
**Precio**: $299.99 - **Stock**: 20 unidades

¿Qué características son más importantes para ti?"""
        
        else:
            return "Puedo ayudarte a encontrar laptops, computadoras, tablets, smartphones, monitores y accesorios. ¿Qué tipo de producto te interesa?"

class ChatService:
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.system_prompt = """Eres un asistente virtual experto de Makers Tech, una tienda especializada en tecnología.

INSTRUCCIONES:
- Responde SIEMPRE en español de forma amable y profesional
- Ayuda a clientes con consultas sobre inventario, características técnicas y precios
- Incluye precios y stock disponible cuando menciones productos
- Ofrece recomendaciones basadas en las necesidades del cliente
- Si no tienes información específica, usa el contexto del inventario proporcionado
- Mantén conversaciones naturales y útiles para ayudar en decisiones de compra

IMPORTANTE AL MOSTRAR PRODUCTOS:
- Cuando te pregunten por productos disponibles, NO envíes toda la información en un solo mensaje largo
- Separa la información de cada producto en párrafos distintos, como si fueras una persona escribiendo
- Para cada producto menciona: nombre/modelo, marca, precio y stock disponible
- Después de mostrar los productos, pregunta si el cliente quiere más detalles sobre alguno específico
- Sé conversacional y natural, no como un catálogo

OBJETIVO: Ser el mejor vendedor virtual que ayude a los clientes a encontrar la tecnología perfecta para sus necesidades."""
        
        if use_mock:
            self.llm = MockChatModel()
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                temperature=0.7, 
                model="gpt-4o",
                api_key=os.getenv("OPENAI_API_KEY")
            )
    
    async def process_message(
        self, 
        message: str,
        inventory_service: Optional[InventoryService] = None,
        recommendation_service: Optional[RecommendationService] = None,
        db_session: Optional[AsyncSession] = None
    ) -> ChatResponse:
        """Procesa un mensaje del usuario y genera una respuesta"""
        
        # Obtener historial de chat reciente (últimos 10 mensajes)
        history_messages = []
        if db_session:
            result = await db_session.execute(
                select(ChatHistory)
                .order_by(ChatHistory.timestamp.desc())
                .limit(10)
            )
            recent_history = result.scalars().all()
            # Revertir para orden cronológico
            for msg in reversed(recent_history):
                if msg.role == "user":
                    history_messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    history_messages.append(AIMessage(content=msg.content))
        
        context = ""
        products_mentioned = []
        
        if inventory_service:
            context = await self._build_context(message, inventory_service)
            products_mentioned = await self._extract_product_ids(message, inventory_service)
            
            # Registrar interacciones y actualizar preferencias
            if recommendation_service:
                await self._track_chat_interactions(
                    message, inventory_service, recommendation_service
                )
        
        # Preparar mensajes para el LLM
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Añadir contexto si existe
        if context:
            messages.append(SystemMessage(content=f"Contexto del inventario:\n{context}"))
        
        # Añadir historial reciente
        messages.extend(history_messages)
        
        # Añadir mensaje actual
        messages.append(HumanMessage(content=message))
        
        # Generar respuesta
        response = await self.llm.agenerate([messages])
        response_text = response.generations[0][0].text
        
        # Guardar en el historial si tenemos sesión de DB
        if db_session:
            # Guardar mensaje del usuario
            user_msg = ChatHistory(
                role="user",
                content=message,
                timestamp=datetime.now()
            )
            db_session.add(user_msg)
            
            # Guardar respuesta del asistente
            assistant_msg = ChatHistory(
                role="assistant",
                content=response_text,
                timestamp=datetime.now(),
                products_mentioned=json.dumps(products_mentioned) if products_mentioned else None
            )
            db_session.add(assistant_msg)
            
            await db_session.commit()
        
        return ChatResponse(
            message=response_text,
            products_mentioned=products_mentioned if products_mentioned else None
        )
    
    async def _build_context(self, message: str, inventory_service: InventoryService) -> str:
        """Construye contexto relevante basado en el mensaje"""
        context_parts = []
        message_lower = message.lower()
        
        # Detectar categorías mencionadas
        category_keywords = {
            "computadora": ProductCategory.COMPUTADORAS,
            "computador": ProductCategory.COMPUTADORAS,
            "desktop": ProductCategory.COMPUTADORAS,
            "pc": ProductCategory.COMPUTADORAS,
            "laptop": ProductCategory.LAPTOPS,
            "portátil": ProductCategory.LAPTOPS,
            "notebook": ProductCategory.LAPTOPS,
            "tablet": ProductCategory.TABLETS,
            "ipad": ProductCategory.TABLETS,
            "teléfono": ProductCategory.CELULARES,
            "celular": ProductCategory.CELULARES,
            "smartphone": ProductCategory.CELULARES,
            "móvil": ProductCategory.CELULARES,
            "monitor": ProductCategory.MONITORES,
            "pantalla": ProductCategory.MONITORES,
            "mouse": ProductCategory.PERIFERICOS,
            "teclado": ProductCategory.PERIFERICOS,
            "periférico": ProductCategory.PERIFERICOS,
            "audífono": ProductCategory.ACCESORIOS,
            "auricular": ProductCategory.ACCESORIOS,
            "webcam": ProductCategory.ACCESORIOS,
            "cámara": ProductCategory.ACCESORIOS,
            "impresora": ProductCategory.IMPRESORAS,
            "printer": ProductCategory.IMPRESORAS
        }
        
        # Buscar productos por categoría
        relevant_categories = set()
        for keyword, category in category_keywords.items():
            if keyword in message_lower:
                relevant_categories.add(category)
        
        # Si se mencionan categorías específicas, obtener productos
        if relevant_categories:
            for category in relevant_categories:
                products = await inventory_service.get_products_by_category(category)
                if products:
                    context_parts.append(f"\nProductos disponibles en {category.value}:")
                    for product in products[:5]:  # Limitar a 5 productos por categoría
                        context_parts.append(
                            f"- {product.name} ({product.brand}): ${product.price} - Stock: {product.stock}"
                        )
        
        # Buscar por marca si se menciona
        brands = ["apple", "samsung", "hp", "dell", "lenovo", "asus", "microsoft", "google", "xiaomi", "oneplus"]
        for brand in brands:
            if brand in message_lower:
                products = await inventory_service.get_products_by_brand(brand.capitalize())
                if products:
                    context_parts.append(f"\nProductos de {brand.capitalize()}:")
                    for product in products[:5]:
                        context_parts.append(
                            f"- {product.name}: ${product.price} - Stock: {product.stock}"
                        )
        
        # Si no hay contexto específico, buscar por términos generales
        if not context_parts:
            search_results = await inventory_service.search_products(message)
            if search_results:
                context_parts.append("\nProductos relacionados con tu búsqueda:")
                for product in search_results[:5]:
                    context_parts.append(
                        f"- {product.name} ({product.brand}): ${product.price} - Stock: {product.stock}"
                    )
        
        return "\n".join(context_parts)
    
    async def _extract_product_ids(self, message: str, inventory_service: InventoryService) -> List[int]:
        """Extrae IDs de productos mencionados en el mensaje"""
        # Por ahora, retornar lista vacía - puede implementarse lógica más compleja
        return []
    
    async def _track_chat_interactions(
        self,
        message: str,
        inventory_service: InventoryService,
        recommendation_service: RecommendationService
    ):
        """Registra interacciones del chat para mejorar recomendaciones"""
        message_lower = message.lower()
        
        # Detectar categorías mencionadas
        category_map = {
            "computadora": "computadoras",
            "computadoras": "computadoras",
            "computador": "computadoras",
            "desktop": "computadoras",
            "pc": "computadoras",
            "laptop": "laptops",
            "laptops": "laptops",
            "portátil": "laptops",
            "portátiles": "laptops",
            "notebook": "laptops",
            "notebooks": "laptops",
            "tablet": "tablets",
            "tablets": "tablets",
            "ipad": "tablets",
            "teléfono": "celulares",
            "teléfonos": "celulares",
            "celular": "celulares",
            "celulares": "celulares",
            "smartphone": "celulares",
            "smartphones": "celulares",
            "móvil": "celulares",
            "iphone": "celulares",
            "galaxy": "celulares",
            "pixel": "celulares",
            "monitor": "monitores",
            "monitores": "monitores",
            "pantalla": "monitores",
            "pantallas": "monitores",
            "mouse": "perifericos",
            "teclado": "perifericos",
            "periférico": "perifericos",
            "periféricos": "perifericos",
            "audífono": "accesorios",
            "audífonos": "accesorios",
            "auricular": "accesorios",
            "auriculares": "accesorios",
            "webcam": "accesorios",
            "cámara": "accesorios",
            "impresora": "impresoras",
            "impresoras": "impresoras",
            "printer": "impresoras"
        }
        
        categories_mentioned = []
        for keyword, category in category_map.items():
            if keyword in message_lower:
                categories_mentioned.append(category)
        
        # Detectar marcas mencionadas
        brands_mentioned = []
        known_brands = ["apple", "samsung", "hp", "dell", "lenovo", "asus", "microsoft", 
                       "google", "xiaomi", "oneplus", "logitech", "corsair", "razer", "benq", "lg"]
        
        for brand in known_brands:
            if brand in message_lower:
                brands_mentioned.append(brand.capitalize())
        
        # Actualizar preferencias basadas en menciones
        if categories_mentioned or brands_mentioned:
            await recommendation_service.update_preferences_from_chat(
                categories_mentioned=list(set(categories_mentioned)),
                brands_mentioned=list(set(brands_mentioned))
            )
        
        # Registrar interacción
        for category in categories_mentioned:
            await recommendation_service.track_interaction(
                interaction_type="chat_mention",
                category=category,
                search_query=message
            ) 