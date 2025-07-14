from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from models.product import Product, ProductCategory
from models.user_interaction import UserInteraction, GlobalUserPreference
from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def track_interaction(
        self, 
        interaction_type: str,
        product_id: Optional[int] = None,
        category: Optional[str] = None,
        search_query: Optional[str] = None
    ):
        """Registra una interacción del usuario sin sesión"""
        interaction = UserInteraction(
            product_id=product_id,
            category_viewed=category,
            search_query=search_query,
            interaction_type=interaction_type,
            timestamp=datetime.now()
        )
        self.session.add(interaction)
        
        # NO actualizar preferencias aquí - se manejan en update_preferences_from_chat
        # await self._update_global_preferences()
        await self.session.commit()
    
    async def _update_global_preferences(self):
        """Actualiza las preferencias globales basándose en todas las interacciones"""
        # Obtener las últimas 100 interacciones
        recent_interactions = await self.session.execute(
            select(UserInteraction)
            .order_by(desc(UserInteraction.timestamp))
            .limit(100)
        )
        interactions = recent_interactions.scalars().all()
        
        category_count = defaultdict(int)
        brand_count = defaultdict(int)
        price_sum = 0
        price_count = 0
        
        for interaction in interactions:
            if interaction.product:
                category_count[interaction.product.category.value] += 1
                brand_count[interaction.product.brand] += 1
                price_sum += interaction.product.price
                price_count += 1
            elif interaction.category_viewed:
                category_count[interaction.category_viewed] += 1
        
        # Determinar preferencias
        preferred_categories = [cat for cat, count in sorted(
            category_count.items(), key=lambda x: x[1], reverse=True
        )[:5]]  # Top 5 categorías
        preferred_brands = [brand for brand, count in sorted(
            brand_count.items(), key=lambda x: x[1], reverse=True
        )[:5]]  # Top 5 marcas
        
        # Calcular rango de precios preferido
        avg_price = price_sum / price_count if price_count > 0 else 1000
        price_min = max(0, avg_price * 0.5)
        price_max = avg_price * 2.0
        
        # Buscar o crear preferencias globales (solo hay un registro)
        pref_result = await self.session.execute(
            select(GlobalUserPreference).limit(1)
        )
        preference = pref_result.scalar_one_or_none()
        
        if not preference:
            preference = GlobalUserPreference()
            self.session.add(preference)
        
        preference.preferred_categories = json.dumps(preferred_categories)
        preference.preferred_brands = json.dumps(preferred_brands)
        preference.price_range_min = price_min
        preference.price_range_max = price_max
        preference.interaction_count = len(interactions)
        preference.last_updated = datetime.now()
    
    async def get_user_preferences(self) -> Optional[Dict]:
        """Obtiene las preferencias globales del usuario"""
        pref_result = await self.session.execute(
            select(GlobalUserPreference).limit(1)
        )
        preference = pref_result.scalar_one_or_none()
        
        if not preference:
            return None
            
        return {
            "preferred_categories": json.loads(preference.preferred_categories) if preference.preferred_categories else [],
            "preferred_brands": json.loads(preference.preferred_brands) if preference.preferred_brands else [],
            "price_range_min": preference.price_range_min,
            "price_range_max": preference.price_range_max,
            "interaction_count": preference.interaction_count
        }
    
    async def get_personalized_recommendations(
        self, 
        limit: int = 12
    ) -> Dict[str, List[Product]]:
        """Obtiene recomendaciones personalizadas basadas en el comportamiento global"""
        
        # Obtener preferencias globales
        pref_result = await self.session.execute(
            select(GlobalUserPreference).limit(1)
        )
        preferences = pref_result.scalar_one_or_none()
        
        # Obtener todos los productos disponibles
        all_products_result = await self.session.execute(
            select(Product).where(Product.is_active == True, Product.stock > 0)
        )
        all_products = list(all_products_result.scalars().all())
        
        # Si no hay preferencias o pocas interacciones, usar algoritmo básico
        if not preferences or preferences.interaction_count < 5:
            return await self._get_default_recommendations(all_products)
        
        # Parsear preferencias
        preferred_categories = json.loads(preferences.preferred_categories) if preferences.preferred_categories else []
        preferred_brands = json.loads(preferences.preferred_brands) if preferences.preferred_brands else []
        
        # Obtener productos vistos recientemente (últimos 30 días)
        recent_views_result = await self.session.execute(
            select(UserInteraction.product_id)
            .where(
                UserInteraction.product_id.is_not(None),
                UserInteraction.timestamp > datetime.now() - timedelta(days=30)
            )
            .distinct()
        )
        recently_viewed_ids = {row[0] for row in recent_views_result}
        
        # Categorizar productos según las últimas categorías buscadas
        highly_recommended = []
        recommended = []
        other_suggestions = []
        
        # Obtener productos de la última categoría buscada
        if len(preferred_categories) > 0:
            last_category = preferred_categories[0].lower()
            for product in all_products:
                if product.category.value.lower() == last_category:
                    highly_recommended.append(product)
                    if len(highly_recommended) >= 6:  # Máximo 6 productos
                        break
        
        # Obtener productos de la penúltima categoría buscada
        if len(preferred_categories) > 1:
            second_last_category = preferred_categories[1].lower()
            for product in all_products:
                if product.category.value.lower() == second_last_category:
                    recommended.append(product)
                    if len(recommended) >= 6:  # Máximo 6 productos
                        break
        
        # Agregar otros productos aleatorios como sugerencias
        used_products = set([p.id for p in highly_recommended + recommended])
        for product in all_products:
            if product.id not in used_products:
                other_suggestions.append(product)
                if len(other_suggestions) >= 6:  # Máximo 6 productos
                    break
        
        return {
            'highly_recommended': highly_recommended,
            'recommended': recommended,
            'other_suggestions': other_suggestions
        }
    
    async def _calculate_product_score(
        self, 
        product: Product,
        preferred_categories: List[str],
        preferred_brands: List[str],
        price_min: float,
        price_max: float,
        already_viewed: bool
    ) -> float:
        """Calcula la puntuación de un producto basándose en las preferencias"""
        score = 0
        
        # Puntuación por categoría (0-35 puntos)
        # Normalizar a minúsculas para comparación
        product_category_lower = product.category.value.lower()
        preferred_categories_lower = [cat.lower() for cat in preferred_categories]
        
        if product_category_lower in preferred_categories_lower:
            # Mayor puntuación para categorías más preferidas
            category_rank = preferred_categories_lower.index(product_category_lower) + 1
            score += max(35 - (category_rank - 1) * 5, 20)
        
        # Puntuación por marca (0-25 puntos)
        if product.brand in preferred_brands:
            brand_rank = preferred_brands.index(product.brand) + 1
            score += max(25 - (brand_rank - 1) * 3, 15)
        
        # Puntuación por rango de precio (0-20 puntos)
        if price_min <= product.price <= price_max:
            score += 20
        elif product.price < price_min:
            # Penalizar productos muy baratos
            price_diff_ratio = (price_min - product.price) / price_min
            score += max(0, 20 - price_diff_ratio * 30)
        else:
            # Penalizar productos muy caros
            price_diff_ratio = (product.price - price_max) / price_max
            score += max(0, 20 - price_diff_ratio * 20)
        
        # Puntuación por disponibilidad (0-15 puntos)
        if product.stock > 10:
            score += 15
        elif product.stock > 5:
            score += 10
        else:
            score += 5
        
        # Puntuación adicional para productos nuevos o trending (0-5 puntos)
        # Por ahora, dar puntos aleatorios basados en el ID
        score += (product.id % 6)
        
        # Penalizar si ya fue visto
        if already_viewed:
            score *= 0.7
        
        return min(100, max(0, score))
    
    async def _get_default_recommendations(
        self, 
        products: List[Product]
    ) -> Dict[str, List[Product]]:
        """Obtiene recomendaciones por defecto cuando no hay suficientes datos"""
        # Agrupar por categoría
        by_category = defaultdict(list)
        for product in products:
            by_category[product.category.value].append(product)
        
        highly_recommended = []
        recommended = []
        other_suggestions = []
        
        # Tomar algunos productos de cada categoría
        for category, category_products in by_category.items():
            # Ordenar por stock y precio
            category_products.sort(key=lambda p: (p.stock, -p.price), reverse=True)
            
            if len(highly_recommended) < 4 and category_products:
                highly_recommended.append(category_products[0])
            elif len(recommended) < 4 and len(category_products) > 1:
                recommended.append(category_products[1])
            elif len(other_suggestions) < 4 and len(category_products) > 2:
                other_suggestions.append(category_products[2])
        
        return {
            'highly_recommended': highly_recommended[:4],
            'recommended': recommended[:4],
            'other_suggestions': other_suggestions[:4]
        }
    
    async def get_related_products(
        self, 
        product_id: int,
        limit: int = 6
    ) -> List[Product]:
        """Obtiene productos relacionados a uno específico"""
        # Obtener el producto
        product_result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product_result.scalar_one_or_none()
        
        if not product:
            return []
        
        # Buscar productos similares
        similar_products_result = await self.session.execute(
            select(Product).where(
                Product.id != product_id,
                Product.is_active == True,
                Product.stock > 0,
                Product.category == product.category
            ).limit(limit * 2)
        )
        similar_products = list(similar_products_result.scalars().all())
        
        # Ordenar por similitud de precio
        similar_products.sort(
            key=lambda p: abs(p.price - product.price)
        )
        
        return similar_products[:limit]
    
    async def update_preferences_from_chat(self, categories_mentioned: List[str], brands_mentioned: List[str]):
        """Actualiza las preferencias basándose en menciones en el chat"""
        # Obtener preferencias actuales
        pref_result = await self.session.execute(
            select(GlobalUserPreference).limit(1)
        )
        preference = pref_result.scalar_one_or_none()
        
        if not preference:
            preference = GlobalUserPreference()
            self.session.add(preference)
            current_categories = []
            current_brands = []
        else:
            current_categories = json.loads(preference.preferred_categories) if preference.preferred_categories else []
            current_brands = json.loads(preference.preferred_brands) if preference.preferred_brands else []
        
        # Normalizar categorías a minúsculas y actualizar
        for category in categories_mentioned:
            category_lower = category.lower()  # Normalizar a minúsculas
            # Remover cualquier versión existente (mayúsculas o minúsculas)
            current_categories = [cat for cat in current_categories if cat.lower() != category_lower]
            # Insertar al principio
            current_categories.insert(0, category_lower)
        
        # Mantener solo las top 2 categorías
        current_categories = current_categories[:2]
        
        # Normalizar marcas y actualizar
        for brand in brands_mentioned:
            brand_normalized = brand.capitalize()  # Normalizar capitalización
            if brand_normalized not in current_brands:
                current_brands.insert(0, brand_normalized)
            else:
                # Mover al principio si ya existe
                current_brands.remove(brand_normalized)
                current_brands.insert(0, brand_normalized)
        
        # Mantener solo las top 3 marcas
        current_brands = current_brands[:3]
        
        preference.preferred_categories = json.dumps(current_categories)
        preference.preferred_brands = json.dumps(current_brands)
        preference.last_updated = datetime.now()
        
        await self.session.commit() 