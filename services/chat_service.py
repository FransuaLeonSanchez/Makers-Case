from typing import List, Dict, Optional, Any
from models.chat import ChatMessage, MessageRole, ChatResponse, ChatHistory, MultiChatResponse
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

INFORMACIÓN DE LA EMPRESA:
- Horarios de atención: Lunes a Viernes de 9:00 AM a 6:00 PM, Sábados de 9:00 AM a 2:00 PM
- Ubicación: Av. Tecnología 123, Ciudad Tech
- Teléfono: +1 (555) 123-4567
- Email: ventas@makerstech.com
- Envíos: A todo el país en 24-48 horas
- Garantía: Todos nuestros productos tienen garantía de 1 año

INSTRUCCIONES IMPORTANTES:
- Responde SIEMPRE en español de forma amable, profesional y CONCISA
- Mantén las respuestas CORTAS y naturales (máximo 2-3 líneas por mensaje)
- Si necesitas mostrar varios productos, SEPARA cada producto en un mensaje diferente
- Actúa como si estuvieras escribiendo en tiempo real, no como un catálogo
- Incluye precios y stock cuando menciones productos específicos
- Si te preguntan por stock específico de un producto, da el número exacto
- Después de mostrar 2-3 productos, pregunta si quieren ver más opciones

FORMATO AL MOSTRAR PRODUCTOS:
- Mensaje 1: Saludo breve + primer producto
- Mensaje 2: Segundo producto (si aplica)
- Mensaje 3: Tercer producto (si aplica)
- Mensaje final: Pregunta si necesitan más información

EJEMPLO DE RESPUESTA MÚLTIPLE:
Usuario: "¿Qué laptops tienen?"
Mensaje 1: "¡Claro! Te muestro nuestras laptops disponibles 💻"
Mensaje 2: "La HP Pavilion 15 es perfecta para trabajo diario - $899.99 (5 unidades)"
Mensaje 3: "También tenemos la MacBook Air M2, ideal si buscas portabilidad - $1499.99 (1 unidad)"
Mensaje 4: "¿Te interesa alguna en particular o quieres ver más opciones?"

INFORMACIÓN DE STOCK:
- Si preguntan cuántas unidades hay de un producto específico, responde con el número exacto
- Si el stock es bajo (menos de 3), menciona que quedan pocas unidades
- Si no hay stock, ofrece alternativas similares

OBJETIVO: Ser un vendedor amigable y eficiente que ayuda con respuestas cortas y claras."""
        
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
    ) -> MultiChatResponse:
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
        
        # Dividir la respuesta en múltiples mensajes si es necesario
        response_messages = self._split_response(response_text)
        
        # Guardar en el historial si tenemos sesión de DB
        if db_session:
            # Guardar mensaje del usuario
            user_msg = ChatHistory(
                role="user",
                content=message,
                timestamp=datetime.now()
            )
            db_session.add(user_msg)
            
            # Guardar cada mensaje de respuesta del asistente
            for msg in response_messages:
                assistant_msg = ChatHistory(
                    role="assistant",
                    content=msg,
                    timestamp=datetime.now(),
                    products_mentioned=json.dumps(products_mentioned) if products_mentioned else None
                )
                db_session.add(assistant_msg)
            
            await db_session.commit()
        
        return MultiChatResponse(
            messages=response_messages,
            products_mentioned=products_mentioned if products_mentioned else None
        )
    
    def _split_response(self, response: str) -> List[str]:
        """Divide una respuesta larga en mensajes más cortos y naturales"""
        # Si la respuesta es corta, no dividir
        if len(response) < 150:
            return [response]
        
        # Buscar mensajes que ya vienen separados por el modelo
        if "Mensaje 1:" in response or "Mensaje 2:" in response:
            # El modelo ya dividió la respuesta
            messages = []
            parts = response.split("Mensaje ")
            for part in parts[1:]:  # Saltar el primer elemento vacío
                if ":" in part:
                    content = part.split(":", 1)[1].strip()
                    messages.append(content)
            return messages if messages else [response]
        
        # Dividir por párrafos o puntos
        paragraphs = response.split('\n\n')
        messages = []
        current_message = ""
        
        for para in paragraphs:
            # Si es una lista de productos, cada producto es un mensaje
            if para.strip().startswith(('1.', '2.', '3.', '-', '•', '*')):
                if current_message:
                    messages.append(current_message.strip())
                    current_message = ""
                
                # Dividir lista en elementos individuales
                items = re.split(r'\n(?=\d+\.|[-•*])', para)
                for item in items:
                    if item.strip():
                        messages.append(item.strip())
            else:
                # Acumular párrafos normales hasta cierto límite
                if len(current_message) + len(para) > 200:
                    if current_message:
                        messages.append(current_message.strip())
                    current_message = para
                else:
                    current_message += "\n\n" + para if current_message else para
        
        # Agregar el último mensaje si queda algo
        if current_message:
            messages.append(current_message.strip())
        
        # Si no se pudo dividir bien, devolver la respuesta original
        return messages if messages else [response]
    
    async def _build_context(self, message: str, inventory_service: InventoryService) -> str:
        """Construye contexto relevante basado en el mensaje"""
        context_parts = []
        message_lower = message.lower()
        
        # Detectar si preguntan por stock específico
        stock_keywords = ["stock", "unidades", "disponible", "disponibles", "quedan", "hay", "tienen", "cuántos", "cuántas"]
        is_stock_query = any(keyword in message_lower for keyword in stock_keywords)
        
        # Detectar productos específicos mencionados por nombre/modelo
        specific_product_keywords = [
            "hp pavilion", "hp probook", "macbook", "zenbook", "thinkpad", "dell xps",
            "iphone", "galaxy", "pixel", "oneplus", "xiaomi",
            "ipad", "surface", "galaxy tab",
            "imac", "optiplex", "elite tower"
        ]
        
        mentioned_products = []
        for keyword in specific_product_keywords:
            if keyword in message_lower:
                products = await inventory_service.search_products(keyword)
                mentioned_products.extend(products)
        
        # Si hay productos específicos mencionados y es consulta de stock
        if mentioned_products and is_stock_query:
            context_parts.append("\nStock específico de productos mencionados:")
            for product in mentioned_products:
                stock_status = "⚠️ Pocas unidades" if product.stock < 3 else "✅ Disponible"
                context_parts.append(
                    f"- {product.name}: {product.stock} unidades {stock_status}"
                )
            return "\n".join(context_parts)
        
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
                        stock_info = f"Stock: {product.stock}"
                        if product.stock < 3:
                            stock_info += " (⚠️ Pocas unidades)"
                        context_parts.append(
                            f"- {product.name} ({product.brand}): ${product.price} - {stock_info}"
                        )
        
        # Buscar por marca si se menciona
        brands = ["apple", "samsung", "hp", "dell", "lenovo", "asus", "microsoft", "google", "xiaomi", "oneplus"]
        for brand in brands:
            if brand in message_lower:
                products = await inventory_service.get_products_by_brand(brand.capitalize())
                if products:
                    context_parts.append(f"\nProductos de {brand.capitalize()}:")
                    for product in products[:5]:
                        stock_info = f"Stock: {product.stock}"
                        if product.stock < 3:
                            stock_info += " (⚠️ Pocas unidades)"
                        context_parts.append(
                            f"- {product.name}: ${product.price} - {stock_info}"
                        )
        
        # Si no hay contexto específico, buscar por términos generales
        if not context_parts:
            search_results = await inventory_service.search_products(message)
            if search_results:
                context_parts.append("\nProductos relacionados con tu búsqueda:")
                for product in search_results[:5]:
                    stock_info = f"Stock: {product.stock}"
                    if product.stock < 3:
                        stock_info += " (⚠️ Pocas unidades)"
                    context_parts.append(
                        f"- {product.name} ({product.brand}): ${product.price} - {stock_info}"
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